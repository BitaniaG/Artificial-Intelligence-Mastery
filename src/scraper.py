import os
import json
import logging
from datetime import datetime
from pathlib import Path

from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv
from tqdm import tqdm

# -------------------------------------------------------------------
# Logging setup
# -------------------------------------------------------------------
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# -------------------------------------------------------------------
# Environment variables
# -------------------------------------------------------------------
load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

if not API_ID or not API_HASH:
    raise ValueError("Missing TELEGRAM_API_ID or TELEGRAM_API_HASH in .env")

# -------------------------------------------------------------------
# Telegram client
# -------------------------------------------------------------------
client = TelegramClient("telegram_session", API_ID, API_HASH)

# -------------------------------------------------------------------
# Channels to scrape
# -------------------------------------------------------------------
CHANNELS = [
    "lobelia4cosmetics",
    "tikvahpharma",
]

# -------------------------------------------------------------------
# Data lake paths (IMPORTANT)
# -------------------------------------------------------------------
RAW_MESSAGES_DIR = Path("data/raw/telegram/messages")
RAW_IMAGES_DIR = Path("data/raw/telegram/images")

RAW_MESSAGES_DIR.mkdir(parents=True, exist_ok=True)
RAW_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------
# Scraping function
# -------------------------------------------------------------------
async def scrape_channel(channel_name: str):
    logging.info(f"Starting scrape for channel: {channel_name}")

    today = datetime.utcnow().strftime("%Y-%m-%d")
    messages_output_dir = RAW_MESSAGES_DIR / today
    images_output_dir = RAW_IMAGES_DIR / channel_name

    messages_output_dir.mkdir(parents=True, exist_ok=True)
    images_output_dir.mkdir(parents=True, exist_ok=True)

    messages_data = []

    async for message in tqdm(
        client.iter_messages(channel_name, limit=200),
        desc=f"Scraping {channel_name}",
    ):
        record = {
            "message_id": message.id,
            "channel_name": channel_name,
            "message_date": message.date.isoformat() if message.date else None,
            "message_text": message.text,
            "views": message.views,
            "forwards": message.forwards,
            "has_media": message.media is not None,
            "image_path": None,
        }

        # Download images if present
        if isinstance(message.media, MessageMediaPhoto):
            image_path = images_output_dir / f"{message.id}.jpg"
            await client.download_media(message.media, image_path)
            record["image_path"] = str(image_path)

        messages_data.append(record)

    output_file = messages_output_dir / f"{channel_name}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(messages_data, f, indent=2, ensure_ascii=False)

    logging.info(
        f"Finished scraping {channel_name}. Messages: {len(messages_data)}"
    )

# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------
async def main():
    async with client:
        for channel in CHANNELS:
            try:
                await scrape_channel(channel)
            except Exception as e:
                logging.exception(f"Error scraping {channel}: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
