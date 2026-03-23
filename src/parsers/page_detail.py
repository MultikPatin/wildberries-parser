import re
from typing import Any

from bs4 import BeautifulSoup

from src.constants import PRODUCT_DESCRIPTION_CLASS, PRODUCT_SPECIFICATION_CLASS


def parse_product_detail(content: str) -> dict[str, Any]:
    soup = BeautifulSoup(content, features="lxml")
    spec = {}

    _spec = parse_description(soup)
    if _spec:
        spec.update(_spec)

    _spec = parse_specification(soup)
    if _spec:
        spec.update(_spec)

    return spec


def parse_description(soup: BeautifulSoup) -> dict[str, Any] | None:
    tag = soup.find("p", class_=PRODUCT_DESCRIPTION_CLASS)
    if not tag:
        return None

    text = tag.get_text(separator=" ", strip=True)
    description = re.sub(r"\s+", " ", text)

    return {"description": description}


def parse_specification(soup: BeautifulSoup) -> dict[str, Any] | None:
    tables = soup.find_all("table", class_=PRODUCT_SPECIFICATION_CLASS)
    if not tables:
        return None

    spec = {}

    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            key_cell = row.find("th")
            value_cell = row.find("td")

            if key_cell and value_cell:
                key = key_cell.get_text(strip=True)
                value = value_cell.get_text(strip=True)
                spec[key] = value

    return {"specification": spec}
