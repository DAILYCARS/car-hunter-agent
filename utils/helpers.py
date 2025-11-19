import re
import logging


def parse_price(text: str) -> int:
    """Wyciąga cenę z tekstu (np. '45 900 zł' → 45900)."""
    if not text:
        return 0

    numbers = re.findall(r"\d+", text.replace(" ", "").replace(",", ""))
    if not numbers:
        return 0

    try:
        return int(numbers[0])
    except Exception as e:
        logging.error(f"Nie mogę sparsować ceny '{text}': {e}")
        return 0


def clean_text(text: str) -> str:
    """Czyści tekst z niepotrzebnych spacji, znaków itp."""
    if not text:
        return ""
    return " ".join(text.split()).strip()


def detect_private_seller(description: str) -> bool:
    """Prosta heurystyka: wykrywa czy ogłoszenie wygląda na prywatne."""
    if not description:
        return False

    private_keywords = [
        "sprzedaję", "sprzedam", "moje auto", "używane przeze mnie",
        "stan jak na zdjęciach", "nie handlarz", "auto rodzinne"
    ]

    return any(kw in description.lower() for kw in private_keywords)
