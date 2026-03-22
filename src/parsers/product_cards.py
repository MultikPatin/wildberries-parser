import re
from typing import Any

from bs4 import BeautifulSoup

from src.constants import (
    PRODUCT_ARTICLE_CLASS,
    PRODUCT_PRICE_CLASS,
    PRODUCT_RATING_CLASS,
    PRODUCT_RATING_PATTERN,
    PRODUCT_REVIEWS_PATTERN,
    PRODUCT_SELLER_CLASS,
    PRODUCT_TITLE_CLASS,
)

# • ! Артикул
# • ! Название
# • ! Цена
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

    _spec = parse_rating_reviews(soup)
    if _spec:
        spec.update(_spec)

    _spec = parse_article(soup)
    if _spec:
        spec.update(_spec)

    _spec = parse_title(soup)
    if _spec:
        spec.update(_spec)

    _spec = parse_price(soup)
    if _spec:
        spec.update(_spec)

    _spec = parse_seller_name(soup)
    if _spec:
        spec.update(_spec)

    return spec


def parse_price(soup: BeautifulSoup) -> dict[str, Any] | None:
    spec = soup.find("ins", class_=PRODUCT_PRICE_CLASS)

    if not (hasattr(spec, "text") and isinstance(spec.text, str)):
        return None

    text = spec.text.strip()
    cleaned = re.sub(r"\D", "", text)
    return {"price": int(cleaned)}


def parse_seller_name(soup: BeautifulSoup) -> dict[str, Any] | None:
    spec = soup.find("span", class_=PRODUCT_SELLER_CLASS)
    if not spec:
        return None

    return {"seller_name": spec.text}


def parse_article(soup: BeautifulSoup) -> dict[str, Any] | None:
    spec = soup.find("span", class_=PRODUCT_ARTICLE_CLASS)
    if not spec:
        return None

    return {"article": spec.text}


def parse_title(soup: BeautifulSoup) -> dict[str, Any] | None:
    spec = soup.find("h2", class_=PRODUCT_TITLE_CLASS)
    if not spec:
        return None

    return {"title": spec.text}


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
