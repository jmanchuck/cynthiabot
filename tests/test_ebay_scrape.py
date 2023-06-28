from bs4 import BeautifulSoup
from src.ebay.completed import parseEbaySoupPrices
from hamcrest import assert_that, equal_to, has_entries, has_key, only_contains


def test_parse_prices(test_ebay_page: str):
    soup = BeautifulSoup(test_ebay_page, "html.parser")

    parsed = parseEbaySoupPrices(soup)

    expected_price_list = [
        195.36,
        235.39,
        251.08,
        313.85,
        375.06,
        470.77,
        508.43,
        784.62,
    ]

    expected_shipping_list = [19.58, 0, 0, 0, 0, 0, 7.85]

    assert_that(parsed, has_key("price-list"))
    assert_that(parsed["price-list"], only_contains(*expected_price_list))

    assert_that(parsed, has_key("shipping-list"))
    assert_that(parsed["shipping-list"], only_contains(*expected_shipping_list))
