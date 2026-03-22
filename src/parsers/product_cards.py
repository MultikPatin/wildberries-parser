import re
from typing import Any

from bs4 import BeautifulSoup
from icecream import ic

from src.constants import (
    PRODUCT_ARTICLE_CLASS,
    PRODUCT_RATING_CLASS,
    PRODUCT_RATING_PATTERN,
    PRODUCT_REVIEWS_PATTERN,
)

# • Ссылка на товар!
# • ! Артикул
# • Название!
# • Цена!
# • Описание
# • Ссылки на изображения через запятую
# • Все характеристики с сохранением их структуры
# • Название селлера!
# • Ссылка на селлера
# • Размеры товара через запятую
# • Остатки по товару (число)
# • ! Рейтинг
# • ! Количество отзывов


def parse_product_card(content: str) -> dict[str, Any]:
    soup = BeautifulSoup(content, features="lxml")
    spec = {}

    # RATING
    r_spec = parse_rating_reviews(soup)
    if r_spec:
        spec.update(r_spec)

    a_spec = parse_article(soup)
    if a_spec:
        spec.update(a_spec)

    ic(spec)
    return spec


def parse_article(soup: BeautifulSoup) -> dict[str, Any] | None:
    spec = soup.find("span", class_=PRODUCT_ARTICLE_CLASS)
    if not spec:
        return None

    return {"article": spec.text}


def parse_rating_reviews(soup: BeautifulSoup) -> dict[str, Any] | None:
    spec = soup.find("span", class_=PRODUCT_RATING_CLASS)

    if not (hasattr(spec, "text") and isinstance(spec.text, str)):
        return None

    text = re.sub(r"\s+", " ", spec.text.strip())

    rating_match = re.search(PRODUCT_RATING_PATTERN, text)
    rating = None
    if rating_match:
        whole = rating_match.group(1)
        fractional = rating_match.group(2) if rating_match.group(2) else "0"
        rating = float(f"{whole}.{fractional}")

    reviews_match = re.search(PRODUCT_REVIEWS_PATTERN, text, re.IGNORECASE)
    reviews_count = None
    if reviews_match:
        reviews_count = int(reviews_match.group(1))

    return {"rating": rating, "reviews_count": reviews_count}
