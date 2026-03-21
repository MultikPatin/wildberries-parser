from collections.abc import Sequence

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from src.constants import (
    PRODUCT_CARD_SIZES,
    PRODUCTS_LIST_CLASS,
    SEARCH_FIELD_ID,
    WB_API_URL,
)

from .driver import get_driver


class WildberriesWebDriver:
    def __init__(self) -> None:
        self._driver = get_driver()
        self._wait = WebDriverWait(self._driver, 10)

    def quit(self) -> None:
        self._driver.quit()

    def get_search_results_html(self, search: str) -> str:
        self._driver.get(WB_API_URL)

        input_field = self._wait.until(
            ec.presence_of_element_located((By.ID, SEARCH_FIELD_ID))
        )

        input_field.send_keys(search)
        input_field.send_keys(Keys.RETURN)

        self._wait.until(
            ec.presence_of_element_located((By.CLASS_NAME, PRODUCTS_LIST_CLASS))
        )
        return self._driver.page_source

    def get_all_product_card_html(self, urls: Sequence[str]) -> list[str]:
        return [self.get_product_card_html(url) for url in urls]

    def get_product_card_html(self, url: str) -> str:
        self._driver.get(url)

        self._wait.until(
            ec.presence_of_element_located((By.CLASS_NAME, PRODUCT_CARD_SIZES))
        )
        return self._driver.page_source
