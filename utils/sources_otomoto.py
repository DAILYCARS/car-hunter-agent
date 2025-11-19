import httpx
import logging
from utils.helpers import parse_price, clean_text

OTOMOTO_URL = "https://www.otomoto.pl/osobowe?search%5Bfilter_float_price%3Afrom%5D=5000&search%5Bfilter_float_price%3Ato%5D=200000"


async def fetch_otomoto():
    """
    Pobiera ogłoszenia z listingu Otomoto (bez API).
    Parsuje tytuł, cenę, link, opis skrócony i info o sprzedawcy.
    """

    logging.info("Scraping Otomoto...")

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(OTOMOTO_URL, headers={
                "User-Agent": "Mozilla/5.0"
            })

    except Exception as e:
        logging.error(f"Otomoto request error: {e}")
        return []

    if response.status_code != 200:
        logging.error(f"Otomoto returned HTTP {response.status_code}")
        return []

    html = response.text

    # ----------------------------------------
    # PROSTE PARSOWANIE (bez JS, bez Playwright)
    # ----------------------------------------
    # Szukamy bloków ogłoszeń
    items = []

    blocks = html.split('data-testid="listing-ad"')
    for block in blocks[1:]:  # pierwszy element to śmieci
        try:
            # LINK
            if 'href="' in block:
                link = block.split('href="')[1].split('"')[0]
                if link.startswith("/"):
                    link = "https://www.otomoto.pl" + link
            else:
                link = None

            # TYTUŁ
            if 'data-testid="ad-title"' in block:
                title = block.split('data-testid="ad-title"')[1]
                title = title.split(">")[1].split("<")[0].strip()
            else:
                title = "Brak tytułu"

            # CENA
            if 'data-testid="ad-price"' in block:
                price_raw = block.split('data-testid="ad-price"')[1]
                price_raw = price_raw.split(">")[1].split("<")[0]
                price = parse_price(price_raw)
            else:
                price = 0

            # SPRZEDAWCA — prywatny / firma
            seller_type = "unknown"
            if "Prywatna" in block or "osoba prywatna" in block.lower():
                seller_type = "private"
            if "Firma" in block:
                seller_type = "dealer"

            # KRÓTKI OPIS (nie zawsze jest)
            if "<p" in block:
                desc = block.split("<p")[1].split(">")[1].split("<")[0]
                description = clean_text(desc)
            else:
                description = ""

            # FILTR NA CENĘ
            if price < 5000 or price > 200000:
                continue

            items.append({
                "source": "otomoto",
                "title": title,
                "price": price,
                "url": link,
                "seller_type": seller_type,
                "description": description
            })

        except Exception as e:
            logging.error(f"Error parsing otomoto block: {e}")
            continue

    logging.info(f"Otomoto found {len(items)} listings.")
    return items
