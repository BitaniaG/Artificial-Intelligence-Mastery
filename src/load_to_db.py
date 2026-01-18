import os
import json
import psycopg2
from datetime import datetime

# Database connection
conn = psycopg2.connect(
    host="localhost",
    port=5433,
    dbname="medical_warehouse",
    user="postgres",
    password="postgres@19"
)

cursor = conn.cursor()

DATA_DIR = "data/raw/telegram_messages"

for date_folder in os.listdir(DATA_DIR):
    date_path = os.path.join(DATA_DIR, date_folder)

    if not os.path.isdir(date_path):
        continue

    for file_name in os.listdir(date_path):
        if not file_name.endswith(".json"):
            continue

        channel_name = file_name.replace(".json", "")
        file_path = os.path.join(date_path, file_name)

        with open(file_path, "r", encoding="utf-8") as f:
            messages = json.load(f)

        for msg in messages:
            cursor.execute(
                """
                INSERT INTO raw.telegram_messages
                (channel_name, message_id, message_date, sender_id, message_text, raw_json)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    channel_name,
                    msg.get("id"),
                    msg.get("date"),
                    msg.get("sender_id"),
                    msg.get("text"),
                    json.dumps(msg)
                )
            )

        print(f"Loaded {len(messages)} messages from {channel_name}")

conn.commit()
cursor.close()
conn.close()

print("✅ Data loading completed.")
