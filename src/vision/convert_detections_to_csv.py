import json
import csv
from pathlib import Path

# Paths
INPUT_JSON = Path("data/enriched/image_detections/detections.json")
OUTPUT_CSV = Path("data/enriched/image_detections/detections.csv")

OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

def main():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        detections = json.load(f)

    if not detections:
        print("No detections found. CSV will be empty.")

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Header
        writer.writerow([
            "channel_name",
            "image_name",
            "object_class",
            "confidence",
            "x_min",
            "y_min",
            "x_max",
            "y_max"
        ])

        for d in detections:
            x_min, y_min, x_max, y_max = d["bbox"]
            writer.writerow([
                d["channel_name"],
                d["image_name"],
                d["object_class"],
                round(d["confidence"], 4),
                x_min,
                y_min,
                x_max,
                y_max
            ])

    print(f"Saved CSV with {len(detections)} rows → {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
