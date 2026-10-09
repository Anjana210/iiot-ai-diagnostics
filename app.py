# app.py
import json
import os
import queue
import paho.mqtt.client as mqtt
import pandas as pd
import streamlit as st
from ai_engine import analyze_telemetry

st.set_page_config(page_title="IIoT AI Diagnostics Dashboard", layout="wide")
st.title("🏭 Real-Time IIoT Asset Diagnostic Center")

# Global thread-safe queue (independent of Streamlit session state)
@st.cache_resource
def get_telemetry_queue():
    return queue.Queue()

telemetry_queue = get_telemetry_queue()

# Initialize Streamlit UI Session State
if "history" not in st.session_state:
    st.session_state.history = []
if "latest_ai" not in st.session_state:
    st.session_state.latest_ai = {
        "status": "HEALTHY",
        "diagnosis": "Awaiting telemetry data...",
    }

# Safe MQTT Callback: Writes strictly to standard Python Queue
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        telemetry_queue.put(payload)
    except Exception as e:
        print(f"Error parsing MQTT message: {e}")

# Start MQTT Client once globally
@st.cache_resource
def start_mqtt_client():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.connect("broker.hivemq.com", 1883, 60)
    client.subscribe("ksa/industrial/sensor_01")
    client.loop_start()
    return client

mqtt_client = start_mqtt_client()

# Drain incoming queue into Streamlit's UI state
while not telemetry_queue.empty():
    new_data = telemetry_queue.get()
    st.session_state.history.append(new_data)
    
    # Keep last 20 readings
    if len(st.session_state.history) > 20:
        st.session_state.history.pop(0)

    # Check metric thresholds to call AI engine
    if (
        new_data["temperature_c"] > 80
        or new_data["pressure_bar"] < 1.0
        or new_data["voltage_v"] > 250
    ):
        st.session_state.latest_ai = analyze_telemetry(new_data)
    else:
        st.session_state.latest_ai = {
            "status": "HEALTHY",
            "diagnosis": "All metrics within operational thresholds.",
        }

# UI Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Live Sensor Metrics")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.line_chart(df.set_index("timestamp")[["temperature_c", "voltage_v"]])
        st.dataframe(df.tail(5), use_container_width=True)
    else:
        st.info("Listening for MQTT messages on topic 'ksa/industrial/sensor_01'...")

with col2:
    st.subheader("AI System Health Status")
    status = st.session_state.latest_ai.get("status", "HEALTHY")

    if status == "CRITICAL":
        st.error(f"Status: {status}")
    else:
        st.success(f"Status: {status}")

    st.info(st.session_state.latest_ai.get("diagnosis"))

# Live Auto-refresh every 3 seconds
@st.fragment(run_every=3)
def auto_refresh():
    st.caption("⚡ Live Streaming (Refreshing every 3s)")

auto_refresh()