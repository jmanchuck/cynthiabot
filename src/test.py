from ebay.scrape import find
from src.util import currency_string
from webhook import send_embedded_message

filtered, url = find("espeon 189")

i = 0
for listing in filtered:
    send_embedded_message(
        title=listing["title"],
        url=listing["viewItemURL"],
        image_url=listing["galleryURL"],
        fields=[
            ("Listing Type", listing["listingInfo"]["listingType"]),
            (
                "Price",
                currency_string(
                    listing["sellingStatus"]["currentPrice"]["value"],
                    listing["sellingStatus"]["currentPrice"]["_currencyId"],
                ),
            ),
        ],
    )
