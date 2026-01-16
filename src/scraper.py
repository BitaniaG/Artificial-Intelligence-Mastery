import os
import json
import logging
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv
from tqdm import tqdm

# Configure logging
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=f"{LOG_DIR}/scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables
load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

if not API_ID or not API_HASH:
    raise ValueError("Telegram API credentials not found in .env file")

# Initialize Telegram client
client = TelegramClient("telegram_session", API_ID, API_HASH)

# Define channels to scrape
CHANNELS = [
    "lobelia4cosmetics",
    "tikvahpharma"
]

# Define WHERE data will be stored
RAW_MESSAGES_DIR = "data/raw/telegram_messages"
RAW_IMAGES_DIR = "data/raw/images"

# scraping function
async def scrape_channel(channel_name):
    logging.info(f"Starting scrape for channel: {channel_name}")

    messages = []
    today = datetime.utcnow().strftime("%Y-%m-%d")

    channel_dir = f"{RAW_MESSAGES_DIR}/{today}"
    image_dir = f"{RAW_IMAGES_DIR}/{channel_name}"

    os.makedirs(channel_dir, exist_ok=True)
    os.makedirs(image_dir, exist_ok=True)

    async for message in client.iter_messages(channel_name, limit=200):
        record = {
            "message_id": message.id,
            "channel_name": channel_name,
            "message_date": message.date.isoformat() if message.date else None,
            "message_text": message.text,
            "views": message.views,
            "forwards": message.forwards,
            "has_media": message.media is not None
        }

        if isinstance(message.media, MessageMediaPhoto):
            image_path = f"{image_dir}/{message.id}.jpg"
            await client.download_media(message.media, image_path)
            record["image_path"] = image_path
        else:
            record["image_path"] = None

        messages.append(record)

    output_file = f"{channel_dir}/{channel_name}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

    logging.info(
        f"Finished scraping {channel_name}. Messages collected: {len(messages)}"
    )

async def main():
    async with client:
        for channel in CHANNELS:
            try:
                await scrape_channel(channel)
            except Exception as e:
                logging.error(f"Error scraping {channel}: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

