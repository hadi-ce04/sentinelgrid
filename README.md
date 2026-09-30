# ⚡ SentinelGrid

### Real-Time Industrial Telemetry & Anomaly Detection

<p align="center">

**Monitor machines. Detect abnormal behavior. Simulate failures. Respond in real time.**

SentinelGrid is a real-time industrial monitoring platform that simulates a fleet of machines, streams live telemetry, detects abnormal operating conditions, and visualizes machine health through an interactive operations dashboard.

</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![WebSockets](https://img.shields.io/badge/WebSockets-Realtime-000000?style=for-the-badge&logo=websocket&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</p>

---

## 🎯 What is SentinelGrid?

Industrial machines constantly generate data.

Temperature.

Vibration.

Current.

RPM.

Pressure.

The difficult part is not collecting the data.

The difficult part is turning that stream of numbers into something an operator can actually understand.

**SentinelGrid explores that problem through a simulated industrial environment.**

The system continuously generates machine telemetry, analyzes the incoming data for abnormal behavior, calculates machine health, and presents everything through a live monitoring dashboard.

It also includes a **fault simulation system**, allowing failures to be introduced intentionally and observed as they propagate through the monitoring pipeline.

---

# 🖥️ Dashboard

The main dashboard provides a live overview of the simulated industrial fleet.

It displays machine status, health, telemetry and active incidents in one place.

![SentinelGrid Dashboard](assets/dashboard.png)

---

# 🚨 Anomaly Detection

When machine telemetry moves outside expected operating conditions, SentinelGrid identifies the abnormal behavior and surfaces it as an incident.

![Anomaly Detection](assets/anomaly-detection.png)

---

# ⚠️ Fault Simulation

Instead of waiting for a failure to happen naturally, the system allows faults to be simulated intentionally.

This makes it possible to test the monitoring pipeline and observe how the system reacts to abnormal machine behavior.

![Fault Simulation](assets/fault-simulation.png)

---

# ✨ Features

## 📡 Real-Time Telemetry

Machines continuously generate simulated operational data including:

- 🌡️ Temperature
- 📳 Vibration
- ⚡ Current
- 🔄 RPM
- ❤️ Machine health
- 🟢 Machine status

Telemetry is continuously streamed to the dashboard.

---

## 🧠 Anomaly Detection

SentinelGrid analyzes incoming telemetry and identifies values that deviate from expected operating conditions.

Detected anomalies can trigger:

- Warning states
- Machine health degradation
- Active incidents
- Visual alerts
- Operator attention

The goal is to demonstrate how raw machine telemetry can be transformed into actionable information.

---

## 🚨 Incident Detection

Instead of simply displaying abnormal numbers, SentinelGrid turns anomalies into operational incidents.

An incident contains information such as:

```text
Machine
↓
Abnormal metric
↓
Detected value
↓
Severity
↓
Timestamp
