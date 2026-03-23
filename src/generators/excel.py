from typing import Any

from openpyxl import Workbook

TITLES = [
    ("article", "Артикул"),
    ("title", "Название товара"),
    ("price", "Цена"),
    ("sizes", "Размеры"),
    ("rating", "Рейтинг"),
    ("reviews_count", "Количество отзывов"),
    ("description", "Описание"),
    ("specification", "Параметры"),
    ("image_urls", "Ссылки на изображения"),
    ("seller_link", "Ссылка продавца"),
    ("seller_name", "Имя Продавца"),
]


def save_products_to_excel(
    products: list[dict[str, Any]], filename: str, sheet_name: str
) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name

    headers = [t[1] for t in TITLES]
    ws.append(headers)

    for product in products:
        row = []
        for attr in [t[0] for t in TITLES]:
            if attr not in product:
                mag = "Некорректный атрибут"
                raise AttributeError(mag)
            row.append(product[attr])
        ws.append(row)

    wb.save(filename)
