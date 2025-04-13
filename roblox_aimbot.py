from ultralytics import YOLO
import mss
import numpy as np
from PIL import Image
import pyautogui
import cv2
import keyboard
import time
import os
from aim_logger import AimLogger

# ========================== CONFIG ==========================
CONFIG = {
    "MODEL_PATH": "best.pt",  # Use "yolov8n.pt" for testing
    "MONITOR": {"top": 0, "left": 0, "width": 2560, "height": 1440},
    "FPS": 30,
    "HEAD_CONFIDENCE": 0.5,
    "AVATAR_CONFIDENCE": 0.6,
    "AIM_DURATION": 0.05,
    "COOLDOWN": 0.4,
    "AUTO_CLICK": False,
    "TRIGGER_KEY": "right",      # Hold right-click to activate
    "TOGGLE_KEY": "caps lock",   # Toggle full aimbot on/off
    "EXIT_KEY": "esc"            # Quit key
}
# ============================================================

# Load YOLO model
try:
    model = YOLO(CONFIG["MODEL_PATH"])
    print(f"✅ Loaded model: {CONFIG['MODEL_PATH']}")
except:
    print("⚠️ best.pt not found. Using yolov8n.pt instead.")
    model = YOLO("yolov8n.pt")

# Init
sct = mss.mss()
logger = AimLogger()
aimbot_enabled = True
last_lock_time = 0
headshot_count = 0
center_screen = (
    CONFIG["MONITOR"]["left"] + CONFIG["MONITOR"]["width"] // 2,
    CONFIG["MONITOR"]["top"] + CONFIG["MONITOR"]["height"] // 2
)

print("🧠 Aimbot ready | Caps Lock = toggle | Right-click = aim | ESC = quit\n")

while True:
    # ====== EXIT, TOGGLE, CONFIRM KEYS ======
    if keyboard.is_pressed(CONFIG["EXIT_KEY"]):
        print("\n👋 Exiting script...")
        break

    if keyboard.is_pressed(CONFIG["TOGGLE_KEY"]):
        aimbot_enabled = not aimbot_enabled
        print(f"\n🔁 Aimbot {'ENABLED' if aimbot_enabled else 'DISABLED'}")
        time.sleep(0.3)

    if keyboard.is_pressed("x"):  # Confirm kill
        logger.update_last_kill(True)
        time.sleep(0.3)
    elif keyboard.is_pressed("z"):  # Confirm miss
        logger.update_last_kill(False)
        time.sleep(0.3)

    # ====== REQUIRE AIMING + Aimbot toggle ======
    if not aimbot_enabled or not keyboard.is_pressed(CONFIG["TRIGGER_KEY"]):
        time.sleep(1 / CONFIG["FPS"])
        continue

    # ====== SCREEN CAPTURE ======
    screenshot = sct.grab(CONFIG["MONITOR"])
    img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
    frame = np.array(img)

    # ====== YOLO PREDICT ======
    results = model.predict(source=frame, conf=0.4, verbose=False)

    # ====== TARGET PRIORITY ======
    head_target = None
    avatar_target = None
    min_head_dist = float('inf')
    min_avatar_dist = float('inf')

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            label = model.names[cls]
            cx = CONFIG["MONITOR"]["left"] + (x1 + x2) // 2
            cy = CONFIG["MONITOR"]["top"] + (y1 + y2) // 2
            dist = ((cx - center_screen[0])**2 + (cy - center_screen[1])**2)**0.5

            # Draw overlay
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Prioritize closest by class
            if label == "Person-Head" and conf > CONFIG["HEAD_CONFIDENCE"] and dist < min_head_dist:
                head_target = (cx, cy, conf, dist, label, cls)
                min_head_dist = dist
            elif label == "Avatar" and conf > CONFIG["AVATAR_CONFIDENCE"] and dist < min_avatar_dist:
                avatar_target = (cx, cy, conf, dist, label, cls)
                min_avatar_dist = dist

    # ====== CHOOSE TARGET & LOCK ======
    target = head_target or avatar_target
    if target:
        now = time.time()
        if now - last_lock_time > CONFIG["COOLDOWN"]:
            pyautogui.moveTo(target[0], target[1], duration=CONFIG["AIM_DURATION"])
            if CONFIG["AUTO_CLICK"]:
                pyautogui.click()

            if target[4] == "Person-Head":
                headshot_count += 1

            last_lock_time = now
            print(f"🎯 {target[4]} | Conf: {target[2]:.2f} | Dist: {int(target[3])} | Headshots: {headshot_count}", end="\r")

            # Log detection + screenshot
            logger.log_detection(
                label=target[4],
                conf=target[2],
                distance=target[3],
                lock_pos=(target[0], target[1]),
                monitor=CONFIG["MONITOR"]
            )

    # ====== CROSSHAIR OVERLAY ======
    cx = CONFIG["MONITOR"]["width"] // 2
    cy = CONFIG["MONITOR"]["height"] // 2
    cv2.drawMarker(frame, (cx, cy), (255, 255, 255), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=1)

    # ====== DISPLAY (OPTIONAL) ======
    cv2.imshow("Roblox Aimbot", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    time.sleep(1 / CONFIG["FPS"])

cv2.destroyAllWindows()
