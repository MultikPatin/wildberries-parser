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
        params = {}

        content = web_driver.get_product_card_html(link)
        if content["content"]:
            page_content = parsers.parse_product_card(content["content"])
            params.update(page_content)
        if content["detail"]:
            page_detail = parsers.parse_product_detail(content["detail"])
            params.update(page_detail)

        ic(params)

    web_driver.quit()


if __name__ == "__main__":
    main()
