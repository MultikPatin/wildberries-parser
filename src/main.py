import logging

from tqdm import tqdm

from src import parsers
from src.constants import FILENAME, SEARCH_QUERY, SHEET_NAME
from src.dtos import Filters, Product
from src.generators.excel import ExcelGenerator
from src.web.wb import WildberriesWebDriver

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Запуск парсера")
    web_driver = WildberriesWebDriver()
    excel_generator = ExcelGenerator(FILENAME)

    total_steps = 3
    with tqdm(total=total_steps, desc="Общий прогресс", unit="этап") as pbar:
        try:
            pbar.set_description("Получение поисковой выдачи")
            content = web_driver.get_search_results_html(SEARCH_QUERY)
            links = parsers.parse_product_links(content) if content else []
            pbar.update(1)

            pbar.set_description("Обработка товаров")
            products = []
            pbar.total += len(links) - 1
            pbar.refresh()

            for link in links:
                params = {}
                card_content = web_driver.get_product_card_html(link)
                if card_content["content"]:
                    page_content = parsers.parse_product_card(
                        card_content["content"]
                    )
                    params.update(page_content)
                if card_content["detail"]:
                    page_detail = parsers.parse_product_detail(
                        card_content["detail"]
                    )
                    params.update(page_detail)
                params.update({"link": link})

                pbar.update(1)
                products.append(Product(**params))

        except Exception:
            logger.exception("Произошла ошибка")
            raise
        finally:
            web_driver.quit()

        pbar.set_description("Сохранение в Excel")
        filters = Filters(min_rating=4.5, max_price=10_000, country="Россия")
        excel_generator.generate(products, SHEET_NAME, filters)
        pbar.update(1)

    logger.info("Парсер завершил работу")


if __name__ == "__main__":
    main()
