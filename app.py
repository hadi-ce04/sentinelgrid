import asyncio
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from anomaly import RollingAnomalyDetector
from simulator import MACHINES, MachineSimulator

app = FastAPI(title="SentinelGrid", version="1.0.0")
BASE = Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")

simulator = MachineSimulator()
detector = RollingAnomalyDetector()
clients = set()
incidents = []

SENSOR_LIMITS = {
    "temperature": (85, 105),
    "vibration": (4, 7),
    "current": (12, 15),
    "rpm": (1400, 1100),
}


def severity(score):
    if score >= 7:
        return "critical"
    if score >= 4.5:
        return "warning"
    return "normal"


def health_for(scores):
    if not scores:
        return 100
    penalty = sum(min(s, 8) for s in scores) * 3
    return max(0, round(100 - penalty))


def make_event(machine):
    values = simulator.sample(machine)
    scores = {}
    statuses = {}

    for sensor, value in values.items():
        score = detector.score(f"{machine}:{sensor}", value)
        scores[sensor] = score
        statuses[sensor] = severity(score)

    worst = max(scores.values())
    worst_sensor = max(scores, key=scores.get)
    state = severity(worst)
    health = health_for(list(scores.values()))

    if state != "normal":
        incidents.insert(0, {
            "machine": machine,
            "sensor": worst_sensor,
            "value": values[worst_sensor],
            "score": worst,
            "severity": state,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        del incidents[25:]

    return {
        "machine": machine,
        "values": values,
        "scores": scores,
        "statuses": statuses,
        "health": health,
        "state": state,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/")
async def root():
    return FileResponse(BASE / "static" / "index.html")


@app.get("/api/machines")
async def machines():
    return {"machines": list(MACHINES)}


@app.get("/api/incidents")
async def get_incidents():
    return {"incidents": incidents}


@app.post("/api/fault/{machine}")
async def fault(machine: str):
    if machine not in MACHINES:
        return {"ok": False, "error": "Unknown machine"}
    simulator.inject_fault(machine)
    return {"ok": True, "machine": machine}


@app.websocket("/ws")
async def websocket(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            await ws.send_json({
                "type": "telemetry",
                "data": [make_event(machine) for machine in MACHINES],
                "incidents": incidents[:12],
            })
            await asyncio.sleep(1)
    except (WebSocketDisconnect, RuntimeError):
        clients.discard(ws)
