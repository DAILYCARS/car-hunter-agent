import asyncio
import logging
from datetime import datetime

from utils.telegram import send_message
from utils.sources import fetch_all_sources
from utils.scoring import evaluate_listing

logging.basicConfig(level=logging.INFO)


async def main_loop():
    logging.info("Agent startuje...")

    while True:
        try:
            logging.info("Pobieranie nowych ogłoszeń...")

            listings = await fetch_all_sources()

            logging.info(f"Pobrano {len(listings)} ogłoszeń. Analizuję...")

            for item in listings:
                score = evaluate_listing(item)

                # Reguły powiadamiania:
                # 1. Cena >= 30% poniżej mediany
                # 2. Prywatny sprzedawca → powiadom niezależnie od ceny
                # 3. Score AI powyżej 60/100
                should_notify = (
                    item.get("is_private") or
                    item.get("is_undervalued") or
                    score >= 60
                )

                if should_notify:
                    msg = format_message(item, score)
                    await send_message(msg)

            logging.info("Analiza zakończona. Czekam 10 minut...\n")
            await asyncio.sleep(600)

        except Exception as e:
            logging.error(f"Błąd główny: {e}")
            await asyncio.sleep(20)


def format_message(item, score):
    """Formatuje wiadomość Telegram."""
    return (
        f"🚗 *Nowa potencjalna okazja!*\n\n"
        f"*Tytuł:* {item.get('title')}\n"
        f"*Cena:* {item.get('price')} zł\n"
        f"*Średnia rynkowa:* {item.get('market_price')} zł\n"
        f"*Różnica:* {item.get('market_delta')}%\n"
        f"*Sprzedawca:* {'Osoba prywatna' if item.get('is_private') else 'Handlarz'}\n"
        f"*Ocena AI:* {score}/100\n\n"
        f"[Otwórz ogłoszenie]({item.get('url')})"
    )


if __name__ == "__main__":
    asyncio.run(main_loop())
