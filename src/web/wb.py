from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from src.constants import (
    CATALOG_ID,
    PRODUCT_SPEC_BUTTON_CLASS,
    PRODUCTS_DETAILS_CONTENT,
    PRODUCTS_PAGE_CONTENT,
    SEARCH_FIELD_ID,
    WB_API_URL,
)

from .driver import get_driver

# TODO Add Exceptions


class WildberriesWebDriver:
    def __init__(self) -> None:
        self._driver = get_driver()
        self._wait = WebDriverWait(self._driver, 10)

    def quit(self) -> None:
        self._driver.quit()

    def _close_cookies(self) -> None:
        method = ec.presence_of_element_located((By.CLASS_NAME, "cookies"))
        cookie_banner = self._wait.until(method)
        close_button = cookie_banner.find_element(By.TAG_NAME, "button")
        close_button.click()
        method = ec.invisibility_of_element_located((By.CLASS_NAME, "cookies"))
        self._wait.until(method)

    def _search_in_catalog(self, search: str) -> None:
        method = ec.presence_of_element_located((By.ID, SEARCH_FIELD_ID))
        input_field = self._wait.until(method)
        input_field.send_keys(search)
        input_field.send_keys(Keys.RETURN)

    def _get_catalog_by_id(self, catalog_id: str) -> str | None:
        method = ec.presence_of_element_located((By.ID, catalog_id))
        catalog_element = self._wait.until(method)
        html = catalog_element.get_attribute("outerHTML")
        return html.strip() if html else None

    def get_search_results_html(self, search: str) -> str | None:
        self._driver.get(WB_API_URL)
        self._close_cookies()
        self._search_in_catalog(search)
        return self._get_catalog_by_id(CATALOG_ID)

    def _get_product_page_content(self, page_content_class: str) -> str | None:
        method = ec.presence_of_element_located(
            (By.CLASS_NAME, page_content_class)
        )
        content = self._wait.until(method)
        html = content.get_attribute("outerHTML")
        return html.strip() if html else None

    def _get_product_detail_content(self, page_detail_class: str) -> str | None:
        method = ec.presence_of_element_located(
            (By.CLASS_NAME, page_detail_class)
        )
        content = self._wait.until(method)
        html = content.get_attribute("outerHTML")
        return html.strip() if html else None

    def get_product_card_html(self, url: str) -> dict[str, str | None]:
        self._driver.get(url)

        page_content = self._get_product_page_content(PRODUCTS_PAGE_CONTENT)

        button = self._driver.find_element(
            By.CLASS_NAME, PRODUCT_SPEC_BUTTON_CLASS
        )
        button.click()

        page_detail = self._get_product_detail_content(PRODUCTS_DETAILS_CONTENT)

        return {"content": page_content, "detail": page_detail}
