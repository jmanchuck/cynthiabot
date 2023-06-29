import logging
from pathlib import Path
from ebaysdk.finding import Connection as Finding

from src.ebay import scrape

logger = logging.getLogger("cynthiabot")

ITEM_KEYS = [
    "title",
    "condition",
    "sellingStatus",
    "listingInfo",
    "itemId",
    "galleryURL",
    "globalId",
    "country",
    "viewItemURL",
]

IGNORE_SEARCH = " -pca -metal -championship -championships -x3 -3x -CGC -PSA -BULK -BGS -ACE -pokegrade -MGC -BUNDLE -SET -graded -grade -complete -grading -korean -damage -damaged -thai -chinese"

config_file_path = Path(scrape.__file__).resolve().parent / "ebay.yaml"

api = Finding(config_file=config_file_path)


def find(query: str, sort_order: str = None, include_auction=True):
    request = {
        "keywords": query + " JAPANESE" + IGNORE_SEARCH,
    }

    if not include_auction:
        request["itemFilter"] = [{"name": "ListingType", "value": ["FixedPrice"]}]

    if sort_order:
        request["sortOrder"] = sort_order

    logger.info(f"Ebay find request: {request}")

    response = api.execute("findItemsByKeywords", request)

    if len(response.dict()) == 0:
        return (
            [],
            f"https://www.ebay.co.uk/sch/i.html?_nkw={request['keywords'].replace(' ', '+')}",
        )

    try:
        filtered = [
            {key: item.get(key, "N/A") for key in ITEM_KEYS}
            for item in response.dict()["searchResult"]["item"]
        ]
    except KeyError:
        logging.error(
            f"Could not find key item in search result = {response.dict()['searchResult']}"
        )
        return (
            [],
            f"https://www.ebay.co.uk/sch/i.html?_nkw={request['keywords'].replace(' ', '+')}",
        )

    return (
        filtered,
        f"https://www.ebay.co.uk/sch/i.html?_nkw={request['keywords'].replace(' ', '+')}",
    )


if __name__ == "__main__":
    response, _ = find("Japanese Pokemon Card", "EndTimeNewest")

    print(", ".join([row["title"] for row in response]))
