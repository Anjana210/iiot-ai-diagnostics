🏭 AI-Integrated Industrial IoT (IIoT) Diagnostic Engine
An end-to-end real-time Industrial IoT diagnostic system that simulates multi-sensor edge telemetry over MQTT, streams real-time telemetry metrics to a Streamlit web dashboard, and leverages Llama-3.3 via Groq API for automated fault detection and root-cause analysis.

🏗️ System Architecture
Plaintext
[ Python Sensor Simulator ] ---> ( MQTT Publisher )
                                       |
                                       v
                             [ HiveMQ Public Broker ]
                                       |
                                       v
                             [ Python AI Ingestion Service ]
                                       |
                                       v
                             [ Groq / Llama-3.3 API ]
                                       |
                                       v
                             [ Streamlit Live Dashboard ]
✨ Features
Real-Time Telemetry Simulation: Simulates industrial hardware streaming temperature, pressure, voltage, and vibration data.

MQTT Event Pipeline: Uses asynchronous publish-subscribe messaging over HiveMQ broker.

AI-Driven Anomaly Detection: Passes telemetry anomalies directly to Llama-3.3 (via Groq API) for instant operational root-cause analysis.

Live Streamlit Dashboard: Interactive live UI displaying streaming line charts and asset status updates.

🛠️ Tech Stack
Language: Python 3.11+

IoT Protocols: MQTT (paho-mqtt)

LLM Engine: Groq API (llama-3.3-70b-versatile)

UI & Data: Streamlit, Pandas

🚀 Quick Start Guide
1. Clone & Install Dependencies
Bash
git clone https://github.com/Anjana210/iiot-ai-diagnostics.git
cd iiot-ai-diagnostics
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
2. Set Your Environment Variable
Set your Groq API key in your terminal session:

PowerShell (Windows):

PowerShell
$env:GROQ_API_KEY="your_groq_api_key_here"
Bash (Linux/Mac):

Bash
export GROQ_API_KEY="your_groq_api_key_here"
3. Run the Dashboard & Simulator
In Terminal 1 (Dashboard):

Bash
streamlit run app.py
In Terminal 2 (Hardware Simulator):

Bash
python simulator.py
