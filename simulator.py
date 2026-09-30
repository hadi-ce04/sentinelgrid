import random
import time

MACHINES = {
    "PUMP-01": {"temperature": 54.0, "vibration": 1.8, "current": 7.4, "rpm": 1740},
    "MOTOR-07": {"temperature": 61.0, "vibration": 2.2, "current": 9.1, "rpm": 1680},
    "COMP-03": {"temperature": 49.0, "vibration": 1.4, "current": 6.8, "rpm": 1820},
    "ARM-12": {"temperature": 43.0, "vibration": 0.9, "current": 4.6, "rpm": 1260},
}

class MachineSimulator:
    def __init__(self):
        self.faults = {}
        self.started = time.time()

    def inject_fault(self, machine):
        self.faults[machine] = time.time()

    def sample(self, machine):
        base = MACHINES[machine]
        fault = machine in self.faults and time.time() - self.faults[machine] < 18
        elapsed = time.time() - self.started

        drift = 0.5 * __import__('math').sin(elapsed / 9)
        values = {
            "temperature": base["temperature"] + drift + random.gauss(0, 0.35),
            "vibration": base["vibration"] + random.gauss(0, 0.08),
            "current": base["current"] + random.gauss(0, 0.18),
            "rpm": base["rpm"] + random.gauss(0, 10),
        }

        if fault:
            values["temperature"] += 18 + random.random() * 8
            values["vibration"] += 3.0 + random.random() * 1.5
            values["current"] += 2.5 + random.random()
            values["rpm"] -= 180 + random.random() * 80

        return {k: round(v, 2) for k, v in values.items()}
