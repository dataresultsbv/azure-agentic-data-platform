import os
import time
import json
import random
from datetime import datetime, timezone, timedelta
from azure.eventhub import EventHubProducerClient, EventData


class Sensor:
    # 3 different temp variables are used:
    # last_temp = the state in memory(used for next calculation)
    # actual_temp = the temp in the actual room(includes drift and recorvery)
    # reported_temp = the temp the sensor outputs(might include anomoly)
    def __init__(self, sensor_meta):
        # Initialize each sensors starting state
        self.sensor_meta = sensor_meta
        self.last_temp = sensor_meta.get("base_temp", 20.0)

        # Track breakdown & hickups
        self.hickup_factor = 1
        self.broken = False

    def generate_sensor_data(self, custom_timestamp):
        # if sensor is already broken, skip
        if self.broken:
            return None

        # small chance that a sensor has a hick-up, chance increases with every hickup
        hickup_chance = 0.0005 * (self.hickup_factor * 2)
        if random.random() < hickup_chance:
            self.hickup_factor += 1
            return None

        # small chance that a sensor breaks down, chance increases exponantially with every hickup
        breakdown_chance = 0.00001 * (self.hickup_factor ** 2)
        if random.random() < breakdown_chance:
            self.broken = True
            return None

        # Get base_temp and determine drift based on sensor_config or default
        base_temp = self.sensor_meta.get("base_temp", 20.0)
        drift_range = self.sensor_meta.get("drift_range", 0.5)

        # Determine if temp goes up or down
        temp_change = random.uniform(-drift_range, drift_range)

        # Mean reversion to prevent temperature drift and keep simulation realistic
        recovery_factor = 0.01
        recovery = (base_temp - self.last_temp) * recovery_factor

        # Set actual temp
        actual_temp = self.last_temp + temp_change + recovery

        # Set reported temp
        reported_temp = actual_temp

        # Simulate an anomaly in temperature measurement
        if random.random() < 0.005:
            anomoly_drift = random.uniform(10.0, 20.0)
            anomoly_change = random.uniform(-anomoly_drift, anomoly_drift)
            reported_temp = actual_temp + anomoly_change

        # Simulate a fire!! Add temperatures to break sensor for next run
        if random.random() < 0.0001:
            reported_temp = 99.99
            actual_temp = 99.99
            self.broken = True

        # Update last_temp
        self.last_temp = actual_temp

        return {
            "sensor_id": self.sensor_meta["id"],
            "timestamp": custom_timestamp.isoformat() + "Z",
            "temperature": round(reported_temp, 2)
        }


class EventHubProducer:
    def __init__(self):
        #Look for ENV variable from runner
        self.CONNECTION_STR = os.getenv("EVENT_HUB_CONNECTION_STR")
        self.EVENT_HUB_NAME = os.getenv("EVENT_HUB_NAME")

        # Setup Event Hub Client
        if self.CONNECTION_STR and self.EVENT_HUB_NAME:
            self.output_to_eventhub = EventHubProducerClient.from_connection_string(
                conn_str=self.CONNECTION_STR,
                eventhub_name=self.EVENT_HUB_NAME
            )
            print(f"Connected to Event Hub: {self.EVENT_HUB_NAME}")
        else:
            self.output_to_eventhub = None
            print("No Event Hub found, Output is send to console alone.")

    def send_batch(self, batch_data):
        # Create an EventDataBatch object to send a batch of events in a single request
        if self.output_to_eventhub:
            event_batch_data = self.output_to_eventhub.create_batch()

            for data in batch_data:
                json_output = json.dumps(data)
                event_batch_data.add(EventData(json_output))

            self.output_to_eventhub.send_batch(event_batch_data)
        # If running locally return the output in the console
        else:
            for data in batch_data:
                print(json.dumps(data))

    def close(self):
        if self.output_to_eventhub:
            self.output_to_eventhub.close()


class Simulation:
    def __init__(self):
        #Look for ENV variable from runner or pick default
        self.BATCH_SIZE = int(os.getenv("BATCH_SIZE", "672"))
        self.CONFIG_PATH = os.getenv("CONFIG_PATH", "src/simulation/sensor_config.json")

        #Open file sensor_config.json
        self.sensors = self.load_config(self.CONFIG_PATH)

        # Convert to Sensor objects
        self.sensor_objects = [Sensor(s) for s in self.sensors]

        # Function spreads the measures over 24 hours. Starting at 00:00:00
        self.start_of_day = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

        self.eventhub = EventHubProducer()

    # Load sensor config into py list with dictionaries
    def load_config(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    def run(self):
        print(f"--- Ingestion started for {len(self.sensor_objects)} sensors and {self.BATCH_SIZE} measurements ---")

        for batch_nr in range(self.BATCH_SIZE):
            # Set time for this batch (each batch is seperated by 15 mins)
            current_batch_time = self.start_of_day + timedelta(minutes=batch_nr * 15)

            # Add a random delta of minutes, seconds and milliseconds to simulate realistic timestamps for each batch
            current_batch_time += timedelta(
                minutes=random.randint(1,3),
                seconds=random.randint(1, 30),
                milliseconds=random.randint(0, 999)
            )

            batch_output = []

            # Loop over each sensor
            for sensor in self.sensor_objects:

                # Add a random delta of minutes, seconds and milliseconds to simulate realistic timestamps for each batch
                time_delta = timedelta(
                    minutes=random.randint(1,3),
                    seconds=random.randint(1, 30),
                    milliseconds=random.randint(0, 999)
                )

                sensor_batch_time = current_batch_time + (time_delta * random.choice([1, -1]))

                # Generate the new data
                data = sensor.generate_sensor_data(sensor_batch_time)

                # Append data only if sensor delivered output
                if data is not None:
                    batch_output.append(data)

            # Send data when batchsize loop is done
            self.eventhub.send_batch(batch_output)

            #Sleep for 0.1 seconds to simulate sensor behaviour and short pauze for CPU control
            time.sleep(0.1)

        self.eventhub.close()


if __name__ == "__main__":
    sim = Simulation()
    sim.run()