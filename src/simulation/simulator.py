import os
import time
import json
import random
from datetime import datetime, timezone, timedelta
from azure.eventhub import EventHubProducerClient, EventData

#Look for ENV variable from runner or pick default
CONNECTION_STR = os.getenv("EVENT_HUB_CONNECTION_STR")
EVENT_HUB_NAME = os.getenv("EVENT_HUB_NAME")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "672"))
CONFIG_PATH = os.getenv("CONFIG_PATH", "src/simulation/sensor_config.json")

# Load sensor config into py list with dictionaries
def load_config(path):
    with open(path, 'r') as f:
        return json.load(f)

def generate_sensor_data(sensor_meta, last_temp, custom_timestamp):
    # Get base_temp and determine drift based on sensor_config or default
    base_temp = sensor_meta.get("base_temp", 20.0)
    drift_range = sensor_meta.get("drift_range", 0.5)
    
    # Determine if temp goes up or down
    temp_change = random.uniform(-drift_range, drift_range)

    # Mean Reversion to prevent temperature drift and keep simulation realistic
    # Calculate how far temp is from base_temp
    # Correct the diversion from base_temp. The further away, the bigger the correction
    recovery_factor = 0.01
    recovery = (base_temp - last_temp) * recovery_factor

    # Set actual temp
    actual_temp = last_temp + temp_change + recovery
    # Set reported temp to use for anomoly, without influencing future measurements
    reported_temp = actual_temp
    
    # Simulate an anomaly in temperature measurement(used for AI detection)
    if random.random() < 0.005:
        # Anamoly changes temp with a random number between 10 and 20
        anomoly_drift = random.uniform(10.0, 20.0)
        # Determine if temp goes up or down
        anomoly_change = random.uniform(-anomoly_drift, anomoly_drift)
        # Set new temp
        reported_temp = actual_temp + anomoly_change

    # Simulate a fire!! Add temperatures to break sensor for next run
    if random.random() < 0.0001:
        reported_temp = 99.99
        actual_temp = 99.99

    #Return output and actual_temp
    return {
        "sensor_id": sensor_meta["id"],
        "timestamp": custom_timestamp.isoformat() + "Z",
        # Reported temp is used below to report the anomoly
        "temperature": round(reported_temp, 2),
    # actual_temp is used below to not influence future measurements by a anomoly
    }, actual_temp

def main():
    #Open de sensor_config.json
    sensors = load_config(CONFIG_PATH)
    
    # Initialize each sensors starting state in key:value pairs
    states = {s["id"]: s["base_temp"] for s in sensors}
    # Function spreads the measures over 24 hours. Starting at 00:00:00
    start_of_day = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Setup Event Hub Client
    if CONNECTION_STR and EVENT_HUB_NAME:
        output_to_eventhub = EventHubProducerClient.from_connection_string(
            conn_str=CONNECTION_STR, eventhub_name=EVENT_HUB_NAME
        )
        print(f"Verbonden met Event Hub: {EVENT_HUB_NAME}")
    else:
        output_to_eventhub = None
        print("No Event Hub found, Output is send to console alone.")

    try:
        print(f"--- Ingestion started for {len(sensors)} sensors and {BATCH_SIZE} measurements ---")

        # Create empty list with sensors that break down
        broken_sensors = []
        # Create dict with all sensors_ids and 1 as multiplier for break-down probability
        hickup_sensors = {sensor_meta["id"]: 1 for sensor_meta in sensors}

        for batch_nr in range(BATCH_SIZE):
            # Set time for this batch (each batch is seperated by 15 mins)
            current_batch_time = start_of_day + timedelta(minutes=batch_nr * 15)
            # Add a random delta of minutes, seconds and milliseconds to simulate realistic timestamps for each batch
            current_batch_time += timedelta(
                minutes=random.randint(1,3),
                seconds=random.randint(1, 30),
                milliseconds=random.randint(0, 999)
                )
            
            # Create an EventDataBatch object to send a batch of events in a single request
            if output_to_eventhub:
                event_batch_data = output_to_eventhub.create_batch()

            # Loop over each sensor
            for sensor_meta in sensors:
                # if sensor is already broken, skip to next sensor
                if sensor_meta["id"] in broken_sensors:
                    continue

                # small chance that a sensor has a hick-up, chance increases exponantially with every hickup
                hickup_chance = 0.0005 * (hickup_sensors[sensor_meta["id"]] * 2)
                if random.random() < hickup_chance:
                    hickup_sensors[sensor_meta["id"]] += 1
                    continue

                # small chance that a sensor breaks down, chance increases exponantially with every hickup
                breakdown_chance = 0.00001 * (hickup_sensors[sensor_meta["id"]] ** 2)
                if random.random() < breakdown_chance:
                    broken_sensors.append(sensor_meta["id"])
                    continue
                
                # Add a random delta of minutes, seconds and milliseconds to simulate realistic timestamps for each batch
                time_delta = timedelta(
                    minutes=random.randint(1,3),
                    seconds=random.randint(1, 30),
                    milliseconds=random.randint(0, 999)
                    )
                sensor_batch_time = current_batch_time + (time_delta * random.choice([1, -1]))
                # Generate the new data and collect the new_temp
                data, new_temp = generate_sensor_data(sensor_meta, states[sensor_meta["id"]], sensor_batch_time)
            
                # After a fire add the sensor to the broken list
                if new_temp == 99.99:
                    if sensor_meta["id"] not in broken_sensors:
                        broken_sensors.append(sensor_meta["id"])

                # Update base_temp with the new_temp to use for next batch run
                states[sensor_meta["id"]] = new_temp
                
                # Output to json format
                json_output = json.dumps(data)
                # Output to eventhub
                if output_to_eventhub:
                    #Add data to EventDataBatch object
                    event_batch_data.add(EventData(json_output))
                # Output to local run
                else:
                    print(json_output)

            # Send data when batchsize loop is done
            if output_to_eventhub:
                output_to_eventhub.send_batch(event_batch_data)
                print(f"Batch ")
        
            #Sleep for 0.1 seconds to simulate sensor behaviour and short pauze for CPU control
            time.sleep(0.1)
    finally:
        if output_to_eventhub:
            output_to_eventhub.close()
    
# Eindoverzicht van de simulatie
    total_sensors = len(sensors)
    num_broken = len(broken_sensors)
    num_active = total_sensors - num_broken
    
    print("\n" + "="*30)
    print("       SIMULATIE RAPPORT")
    print("="*30)
    print(f"Totaal aantal sensoren: {total_sensors}")
    print(f"Actieve sensoren:       {num_active}")
    print(f"Defecte sensoren:       {num_broken}")
    
    if num_broken > 0:
        print(f"Lijst met defecte ID's: {', '.join(broken_sensors)}")
    
    # Bereken het uitvalpercentage
    failure_rate = (num_broken / total_sensors) * 100
    print(f"Uitvalpercentage:       {failure_rate:.2f}%")
    print("="*30)
    
    print(f"--- Ingestion completed ---")

if __name__ == "__main__":
    main()