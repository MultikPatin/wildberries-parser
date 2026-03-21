from dataclasses import dataclass

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
    description: str
    image_url: str
    spec: str
    seller_name: str
    seller_link: str
    sizes: list[str]
    balance: int
    rating: int
    number_of_reviews: int
