from dataclasses import dataclass
from typing import Any

# Список нужных данных:
# • Ссылка на товар
# • Артикул
# • Название
# • Цена
# • Описание
# • Ссылки на изображения через запятую
# • Все характеристики с сохранением их структуры
# • Название селлера
# • Ссылка на селлера
# • Размеры товара через запятую
# • Остатки по товару (число)
# • Рейтинг
# • Количество отзывов


@dataclass
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
    balance: int
    rating: float | None = None
    reviews_count: int | None = None
