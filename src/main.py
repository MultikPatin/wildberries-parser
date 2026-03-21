from src import parser
from src.constants import SEARCH_QUERY
from src.web.wb import WildberriesWebDriver


def main() -> None:
    web_driver = WildberriesWebDriver()

    content = web_driver.get_search_results_html(SEARCH_QUERY)
    links = parser.extract_product_links(content)

    product_contents = web_driver.get_all_product_card_html(links)

    for product_content in product_contents:
        parser.extract_product_cards_spec(product_content)

    web_driver.quit()


if __name__ == "__main__":
    main()
