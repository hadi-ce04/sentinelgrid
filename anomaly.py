from collections import deque
import math


class RollingAnomalyDetector:
    def __init__(self, window=60):
        self.window = window
        self.history = {}

    def score(self, key, value):
        values = self.history.setdefault(key, deque(maxlen=self.window))

        if len(values) < 8:
            values.append(value)
            return 0.0

        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        std = math.sqrt(variance)
        score = abs(value - mean) / max(std, 0.05)
        values.append(value)
        return round(score, 2)
