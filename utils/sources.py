import logging
from utils.helpers import clean_text, parse_price, detect_private_seller
from utils.market import compute_market_price, market_delta

# 👉 Importy scraperów (na razie jeden przykład – Otomoto)
from utils.sources_otomoto import fetch_otomoto


async def fetch_all_sources():
    """
    Pobiera ogłoszenia ze wszystkich serwisów.
    Na razie mamy Otomoto jako przykład.
    Kolejne dodamy jako osobne pliki.
    """

    listings = []

    try:
        otomoto_results = await fetch_otomoto()
        listings.extend(otomoto_results)
    except Exception as e:
        logging.error(f"Otomoto scraper error: {e}")

    # Tu dodamy później:
    # - fetch_olx()
    # - fetch_allegro()
    # - fetch_mobile_de()
    # - itd.
    # listings.extend(await fetch_olx())
    # listings.extend(await fetch_sprzedajemy())

    # Jeśli brak danych – nic nie robimy
    if not listings:
        return []

    # Liczenie mediany rynku
    prices = [item["price"] for item in listings if item["price"] > 0]
    market_price = compute_market_price(prices)

    # Przetwarzanie ofert i dodanie metadanych
    final_listings = []

    for item in listings:
        price = item["price"]
        delta = market_delta(price, market_price)

        item["market_price"] = market_price
        item["market_delta"] = delta
        item["is_undervalued"] = delta <= -30

        # Wykrywamy prywatnego sprzedawcę
        desc = clean_text(item.get("description", ""))
        item["is_private"] = detect_private_seller(desc) or item.get("seller_type") == "private"

        final_listings.append(item)

    return final_listings
