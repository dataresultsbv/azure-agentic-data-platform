import os
import time
import json
import random
from datetime import datetime

#Look for ENV variable from runner or pick default
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 10))
CONFIG_PATH = os.getenv("CONFIG_PATH", "src/simulation/sensors_config.json")

# Load sensor config into py list with dictionaries
def load_config(path):
    with open(path, 'r') as f:
        return json.load(f)

def generate_sensor_data(sensor_meta, last_temp):
    # Determine drift based on sensor_config or default
    drift = sensor_meta.get("drift_range", 0.5)
    # Determine if temp goes up or down
    temp_change = random.uniform(-drift, drift)
    # Set new temp
    new_temp = last_temp + temp_change
    
    # Simulate an anomaly with a change of 2 percent(used for AI detection)
    if random.random() < 0.2:
        # Anamoly changes temp with a random number between 10 and 20
        anomoly_drift = random.uniform(10.0, 20.0)
        # Determine if temp goes up or down
        anomoly_change = random.uniform(-anomoly_drift, anomoly_drift)
        # Set new temp
        new_temp += anomoly_change

    #Return output and new_temp
    return {
        "sensor_id": sensor_meta["id"],
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "temperature": round(new_temp, 2),
    }, new_temp

def main():
    #Open de sensor_config.json
    sensors = load_config(CONFIG_PATH)
    
    # Initialize each sensors starting state in key:value pairs
    states = {s["id"]: s["base_temp"] for s in sensors}

    print(f"--- Ingestion started for {len(sensors)} sensors and {BATCH_SIZE} measurements ---")

    for r in range(BATCH_SIZE):
        for sensor_meta in sensors:
            s_id = sensor_meta["id"]
            
            # Generate the new data and collect the new_temp to save in the states dict below
            data, new_temp = generate_sensor_data(sensor_meta, states[s_id])
            
            # Update base_temp with the new_temp to use for next batch run
            states[s_id] = new_temp
            
            # Output the data to stdout with print() for logging purposes
            print(json.dumps(data))
        
        #Sleep for 0.1 seconds to simulate sensor behaviour and short pauze for CPU control
        time.sleep(0.1)

    print(f"--- Ingestion completed ---")

if __name__ == "__main__":
    main()