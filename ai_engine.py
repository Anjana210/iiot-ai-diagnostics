# ai_engine.py
import json
import os
from groq import Groq

# Pulls API key from system environment variable GROQ_API_KEY
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analyze_telemetry(telemetry_data):
    prompt = f"""
    You are an Industrial Reliability Engineer for utility assets.
    Analyze this real-time telemetry payload from device '{telemetry_data["device_id"]}':
    
    Data: {json.dumps(telemetry_data)}
    
    Thresholds:
    - Normal Temp: 30-75 °C
    - Normal Pressure: 1.5-5.0 bar
    - Normal Voltage: 200-240 V
    
    Respond strictly in JSON format with two keys:
    1. "status": "NORMAL" or "CRITICAL"
    2. "diagnosis": Short root cause analysis and action plan (max 2 sentences).
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)