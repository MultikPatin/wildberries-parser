from typing import TYPE_CHECKING

from selenium import webdriver

if TYPE_CHECKING:
    from selenium.webdriver.chrome.webdriver import WebDriver


def get_driver() -> "WebDriver":
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")

    return webdriver.Chrome(options=options)
