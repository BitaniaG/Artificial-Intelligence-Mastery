from ultralytics import YOLO
from pathlib import Path
import json

# Paths
IMAGE_ROOT = Path("data/raw/telegram/images")
OUTPUT_DIR = Path("data/enriched/image_detections")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "detections.json"

# Load YOLOv8 pretrained model
model = YOLO("yolov8n.pt")  # nano = fast + lightweight

results_list = []

for channel_dir in IMAGE_ROOT.iterdir():
    if not channel_dir.is_dir():
        continue

    channel_name = channel_dir.name

    for image_path in channel_dir.glob("*"):
        if image_path.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
            continue

        results = model(image_path, verbose=False)

        for r in results:
            for box in r.boxes:
                results_list.append({
                    "channel_name": channel_name,
                    "image_name": image_path.name,
                    "object_class": model.names[int(box.cls)],
                    "confidence": float(box.conf),
                    "bbox": box.xyxy.tolist()[0]
                })

# Save results
with open(OUTPUT_FILE, "w") as f:
    json.dump(results_list, f, indent=2)

print(f"Saved {len(results_list)} detections to {OUTPUT_FILE}")
