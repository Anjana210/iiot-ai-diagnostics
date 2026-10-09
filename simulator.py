# simulator.py
import json
import random
import time
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"  # Free public MQTT broker
PORT = 1883
TOPIC = "ksa/industrial/sensor_01"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT, 60)

print("Starting Industrial Sensor Simulation...")

while True:
    # Baseline normal values
    temperature = round(random.uniform(40.0, 65.0), 2)
    pressure = round(random.uniform(2.0, 4.5), 2)
    voltage = round(random.uniform(210.0, 230.0), 2)
    vibration = round(random.uniform(0.1, 0.5), 2)

    # 10% chance to simulate a hardware anomaly / breakdown
    if random.random() < 0.10:
        anomaly_type = random.choice(["OVERHEAT", "PRESSURE_DROP", "VOLTAGE_SPIKE"])
        if anomaly_type == "OVERHEAT":
            temperature = round(random.uniform(95.0, 120.0), 2)
        elif anomaly_type == "PRESSURE_DROP":
            pressure = round(random.uniform(0.1, 0.8), 2)
        elif anomaly_type == "VOLTAGE_SPIKE":
            voltage = round(random.uniform(270.0, 310.0), 2)

    payload = {
        "device_id": "SMARTEX-PX-01",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "temperature_c": temperature,
        "pressure_bar": pressure,
        "voltage_v": voltage,
        "vibration_g": vibration,
    }

    client.publish(TOPIC, json.dumps(payload))
    print(f"Published: {payload}")
    time.sleep(3)  # Send payload every 3 seconds