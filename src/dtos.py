from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Product:
    link: str
    article: str
    title: str
    price: int
    description: str
    specification: dict[str, Any]
    image_urls: str
    seller_name: str
    seller_link: str
    sizes: list[str]
    rating: float | None = None
    reviews_count: int | None = None


@dataclass(frozen=True)
class Filters:
    min_rating: float | None = None
    max_price: int | None = None
    country: str | None = None
