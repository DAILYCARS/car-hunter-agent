import statistics


def compute_market_price(history: list[int]) -> int:
    """
    Liczy medianę cenową rynku, bazując na historii cen tego modelu.
    history: lista cen z ostatnich ogłoszeń (np. 15–30 pozycji).

    Zwraca liczbę (średnia / mediana).
    """

    if not history:
        return 0

    # Mediana działa lepiej niż średnia — odporna na zawyżone ceny handlarzy
    try:
        median_price = int(statistics.median(history))
        return median_price
    except:
        return 0


def market_delta(price: int, market_price: int) -> float:
    """
    Zwraca różnicę procentową między ceną a medianą rynku.
    Np. -32.4 oznacza 32% poniżej rynku.
    """

    if not price or not market_price:
        return 0

    try:
        return round(((price - market_price) / market_price) * 100, 2)
    except:
        return 0
