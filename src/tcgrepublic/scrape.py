from pprint import pprint
import re
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

REMOVE_ENDS = ["V", "VMAX", "GX", "EX"]


def pokemon_special_art_url(page=1):
    return f"https://tcgrepublic.com/product/tag_page.html?p={page}&tags=3475"


def get_html(url):
    print(f"HTML url: {url}")

    # Get the web page HTML
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response, "html.parser")

    return soup


def parse_items(soup: BeautifulSoup):
    search_results = soup.find("ul", {"id": "search_result_products"})
    raw_items = search_results.find_all("div", {"class": "product_thumbnail_caption"})

    parsed_items = []

    for item in raw_items:
        thumbnail_text = item.find("span").get_text()
        pattern = r"(.*?)(\d{3}/\d{3})"

        match = re.search(pattern, thumbnail_text)

        if match:
            full_text = match.group(1).strip()
            number = match.group(2)

            if not full_text.isascii():
                print(f"Non alphanumeric text {thumbnail_text}")
                continue
            parsed_items.append((full_text, number))
        else:
            print(f"Failed to parse {thumbnail_text}")

    pprint(parsed_items)
    return parsed_items


if __name__ == "__main__":
    parse_items(get_html(pokemon_special_art_url(1)))
