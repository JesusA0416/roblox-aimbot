import json
import os
import time
from datetime import datetime
import pyautogui

class AimLogger:
    def __init__(self, save_dir="aim_logs"):
        self.save_dir = save_dir
        self.log_path = os.path.join(save_dir, "log.json")
        os.makedirs(save_dir, exist_ok=True)
        self.data = []

        # Load existing log if it exists
        if os.path.exists(self.log_path):
            with open(self.log_path, "r") as f:
                self.data = json.load(f)

    def log_detection(self, label, conf, distance, lock_pos, monitor):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{label}_{timestamp}.png"
        filepath = os.path.join(self.save_dir, filename)

        # Capture screenshot
        pyautogui.screenshot(filepath, region=(
            monitor["left"],
            monitor["top"],
            monitor["width"],
            monitor["height"]
        ))

        # Save metadata
        entry = {
            "timestamp": timestamp,
            "class": label,
            "confidence": conf,
            "distance": distance,
            "lock_position": lock_pos,
            "screenshot": filename,
            "was_kill": None  # Optional: update manually
        }
        self.data.append(entry)
        self.save_log()
        print(f"📸 Logged {label} @ {int(distance)}px | {conf:.2f}")

    def save_log(self):
        with open(self.log_path, "w") as f:
            json.dump(self.data, f, indent=2)

    def update_last_kill(self, result: bool):
        if self.data:
            self.data[-1]["was_kill"] = result
            self.save_log()
            print(f"🔁 Updated last entry: was_kill = {result}")
