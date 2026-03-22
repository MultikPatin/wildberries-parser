from icecream import ic

from src import parsers
from src.web.wb import WildberriesWebDriver

SEARCH_QUERY = "пальто из натуральной шерсти"


def main() -> None:
    web_driver = WildberriesWebDriver()

    links = []
    content = web_driver.get_search_results_html(SEARCH_QUERY)
    if content:
        links = parsers.parse_product_links(content)

    for link in links:
        content = web_driver.get_product_card_html(link)
        if content["page_content"]:
            page_content = parsers.parse_product_card(content["page_content"])

        ic(page_content)

    web_driver.quit()


if __name__ == "__main__":
    main()
