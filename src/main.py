from icecream import ic

from src import parsers
from src.constants import SEARCH_QUERY
from src.web.wb import WildberriesWebDriver


def main() -> None:
    web_driver = WildberriesWebDriver()

    content = web_driver.get_search_results_html(SEARCH_QUERY)
    links = parsers.parse_product_links(content)

    for link in links:
        product_content = web_driver.get_product_card_html(link)
        spec = parsers.parse_product_card(product_content)
        ic(spec)

    web_driver.quit()


if __name__ == "__main__":
    main()
