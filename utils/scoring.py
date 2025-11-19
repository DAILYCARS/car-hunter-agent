def evaluate_listing(item: dict) -> int:
    """
    Zwraca ocenę "okazji" w skali 0–100.
    To uproszczona wersja — później można ją ulepszyć.
    """

    score = 0

    # 1. Silny punkt za bycie osobą prywatną
    if item.get("is_private"):
        score += 30

    # 2. Cena mocno poniżej rynku
    delta = item.get("market_delta", 0)  # np. -32%

    if delta <= -30:
        score += 40
    elif delta <= -20:
        score += 25
    elif delta <= -10:
        score += 10

    # 3. Im wyższa jakość opisu, tym lepiej
    desc = item.get("description", "")
    if len(desc) > 500:
        score += 10
    elif len(desc) > 200:
        score += 5

    # 4. Drobne bonusy
    if "serwis" in desc.lower():
        score += 5
    if "niewypadkowy" in desc.lower():
        score += 5

    # Upewniamy się, że wynik mieści się w zakresie 0–100
    return max(0, min(100, score))
