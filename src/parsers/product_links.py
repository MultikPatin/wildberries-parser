from bs4 import BeautifulSoup, Tag

from src.constants import PRODUCT_CARD_CLASS, PRODUCT_CARD_LINK_CLASS


def parse_product_links(content: str) -> list[str]:
    soup = BeautifulSoup(content, features="lxml")

    product_links = []
    cards = soup.find_all(class_=PRODUCT_CARD_CLASS)

    for card in cards:
        link = _get_link(card)
        if link:
            product_links.append(link)

    return product_links


def _get_link(soap: Tag) -> str | None:
    tag = soap.find("a", class_=PRODUCT_CARD_LINK_CLASS)
    if tag and tag.get("href"):
        return str(tag.get("href"))
    return None
