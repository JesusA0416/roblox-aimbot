# 🔫 Roblox Gunfight Arena Aimbot

This is a YOLOv8-based aimbot created for Roblox FPS games like **Gunfight Arena**. It automatically detects and locks onto enemies using real-time object detection, with head prioritization, adaptive logging, and training pipeline support.

---

## ⚙️ Features

- 🎯 **YOLOv8 Detection** (Person-Head & Avatar)
- 🖱️ Right-click activated (aim only when scoped)
- 🔄 Caps Lock toggles aimbot on/off
- 🧠 Prioritizes closest target to crosshair
- 💻 ESC exits script instantly
- ⚡ FPS limiter + cooldown timer
- 💥 Auto-click (optional)
- 📸 Screenshots saved on lock
- 📊 `log.json` file tracks distance, confidence, timestamp
- 🧪 Manual feedback: Press `X` = kill, `Z` = miss

---

## 🛠 Requirements

- Python 3.11+
- `pip install -r requirements.txt`

---

## 🔧 Hotkeys

| Key          | Function                 |
|--------------|--------------------------|
| Right-click  | Activate aimbot (ADS)    |
| Caps Lock    | Toggle aimbot ON/OFF     |
| X            | Mark last lock as **Kill** |
| Z            | Mark last lock as **Miss** |
| ESC          | Quit the script          |

---

## 📁 Folder Structure


---

## 🚀 How to Run

1. Place `best.pt` (or test with `yolov8n.pt`) in the same folder.
2. Open a terminal and run:

```bash
python roblox_aimbot.py
