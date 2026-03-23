from datetime import datetime

WB_API_URL = "https://www.wildberries.ru"

SEARCH_QUERY = "пальто из натуральной шерсти"
FILENAME = (
    f"Выгрузка_{SEARCH_QUERY.replace(' ', '_')}"
    f"_{datetime.now().strftime('%Y.%m.%d-%H_%M_%S')}.xlsx"
)
SHEET_NAME = "Продукты"

SEARCH_FIELD_ID = "searchInput"
CATALOG_ID = "catalog"

PRODUCT_SPEC_BUTTON_CLASS = "btnDetail--im7UR"
PRODUCTS_PAGE_CONTENT = "productPageContent--jaf94"
PRODUCTS_DETAILS_CONTENT = "detailsModal--eHzZX"

# ---------------------------------------------------

PRODUCT_CARD_CLASS = "product-card"
PRODUCT_CARD_LINK_CLASS = "product-card__link"

# ---------------------------------------------------

PRODUCT_ARTICLE_CLASS = "cellCopy--sPwsd"
PRODUCT_SIZES_CLASS = "sizesListItem--QcbQx"
PRODUCT_SIZE_CLASS = "sizesListSize--NUoNC"
PRODUCT_SELLER_NAME_CLASS = "sellerInfoNameDefaultText--qLwgq"
PRODUCT_SELLER_CLASS = "sellerInfoButtonLink--RoLBz"
PRODUCT_RATING_CLASS = "productReviewRating--PD7fr"
PRODUCT_TITLE_CLASS = "productTitle--lfc4o"
PRODUCT_PRICE_CLASS = "priceBlockFinalPrice--iToZR"
PRODUCT_IMAGES_CLASS = "swiper-slide mainSlide--TIHn4"

# ---------------------------------------------------

PRODUCT_DESCRIPTION_CLASS = "descriptionText--Jq9n2"
PRODUCT_SPECIFICATION_CLASS = "table--tSF0X table--CGApj"

# ---------------------------------------------------

PRODUCT_RATING_PATTERN = r"(\d+)(?:,(\d))?"
PRODUCT_REVIEWS_PATTERN = r"(\d+)\s*\D*оценок|\d+\s*\D*отзывов"
