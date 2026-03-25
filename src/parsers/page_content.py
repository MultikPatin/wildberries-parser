import re
from typing import Any

from bs4 import BeautifulSoup

from src.constants import (
    PRODUCT_ARTICLE_CLASS,
    PRODUCT_IMAGES_CLASS,
    PRODUCT_PRICE_CLASS,
    PRODUCT_RATING_CLASS,
    PRODUCT_RATING_PATTERN,
    PRODUCT_REVIEWS_PATTERN,
    PRODUCT_SELLER_CLASS,
    PRODUCT_SELLER_NAME_CLASS,
    PRODUCT_SIZES_CLASS,
    PRODUCT_TITLE_CLASS,
    WB_API_URL,
)


def parse_product_card(content: str) -> dict[str, Any]:
    soup = BeautifulSoup(content, features="lxml")
    spec = {}

    funcs = (
        parse_image_urls,
        parse_rating_reviews,
        parse_seller_name,
        parse_seller_link,
        parse_article,
        parse_title,
        parse_price,
        parse_sizes,
    )

    for func in funcs:
        res = func(soup)
        if res:
            spec.update(res)

    return spec


def parse_sizes(soup: BeautifulSoup) -> dict[str, Any] | None:
    size_items = soup.find_all("li", class_=PRODUCT_SIZES_CLASS)
    if not size_items:
        return None

    sizes = []
    for item in size_items:
        span = item.find("span")
        if span:
            size_text = span.get_text(strip=True)
            if size_text:
                sizes.append(size_text)

    return {"sizes": sizes}


def parse_image_urls(soup: BeautifulSoup) -> dict[str, list[str]] | None:
    elements = soup.find_all("div", class_=PRODUCT_IMAGES_CLASS)

    if not elements:
        return None

    urls = []
    for element in elements:
        img = element.find("img")
        if not img:
            continue

        urls.append(img.get("src"))

    unique_urls = list(dict.fromkeys(urls))

    return {"image_urls": unique_urls}


def parse_price(soup: BeautifulSoup) -> dict[str, Any] | None:
    spec = soup.find("ins", class_=PRODUCT_PRICE_CLASS)

    if not (hasattr(spec, "text") and isinstance(spec.text, str)):
        return None

    text = spec.text.strip()
    cleaned = re.sub(r"\D", "", text)
    return {"price": int(cleaned)}


def parse_seller_link(soup: BeautifulSoup) -> dict[str, Any] | None:
    tag = soup.find("a", class_=PRODUCT_SELLER_CLASS)
    if not tag:
        return None

    sub = tag.get("href")
    if not sub:
        return None

    return {"seller_link": WB_API_URL + str(sub)}


def parse_seller_name(soup: BeautifulSoup) -> dict[str, Any] | None:
    spec = soup.find("span", class_=PRODUCT_SELLER_NAME_CLASS)
    if not spec:
        return None

    return {"seller_name": spec.text}


def parse_article(soup: BeautifulSoup) -> dict[str, Any] | None:
    tag = soup.find("button", class_=PRODUCT_ARTICLE_CLASS)
    if not tag:
        return None

    return {"article": tag.text}


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
