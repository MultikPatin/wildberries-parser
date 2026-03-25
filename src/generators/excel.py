import re
from dataclasses import asdict
from typing import Any

import pandas as pd

from src.constants import COLUMNS_TITLES
from src.dtos import Filters, Product


class ExcelGenerator:
    def __init__(self, filename: str) -> None:
        self._filename = _sanitize_filename(filename)
        self._columns = [x[1] for x in COLUMNS_TITLES]
        self._attrs = [x[0] for x in COLUMNS_TITLES]

    def generate(
        self, products: list[Product], sheet_name: str, filters: Filters
    ) -> None:
        if not products:
            df = pd.DataFrame(columns=self._attrs)
        else:
            rows = _parse_products(products)
            df = pd.DataFrame(rows, columns=self._attrs)

        df = self._filter(df, filters)
        df.columns = self._columns
        df.to_excel(self._filename, index=False, sheet_name=sheet_name)

    def _filter(self, df: pd.DataFrame, filters: Filters) -> pd.DataFrame:
        if filters.min_rating is not None:
            df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
            df = df[df["rating"] >= filters.min_rating]

        if filters.max_price is not None:
            df["price"] = pd.to_numeric(df["price"], errors="coerce")
            df = df[df["price"] <= filters.max_price]

        if filters.country is not None:
            df = df[
                df["specification"]
                .astype(str)
                .str.contains(filters.country, na=False)
            ]

        return df[self._attrs]


def _sanitize_filename(filename: str) -> str:
    return re.sub(r'[<>:"/\\|?*\']', "_", filename)


def _parse_products(products: list[Product]) -> list[dict[str, Any]]:
    return [asdict(product) for product in products]
