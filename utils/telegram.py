import os
import aiohttp
import logging

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


async def send_message(text: str):
    """Wysyła wiadomość do Telegrama."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logging.error("Brak TELEGRAM_TOKEN lub TELEGRAM_CHAT_ID w zmiennych środowiskowych.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            if resp.status != 200:
                logging.error(f"Telegram error: {resp.status}")
