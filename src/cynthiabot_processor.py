from src.ebay.completed import averageEbayPrices


def psa_ebay_average(query: str, grade: int):
    query = f"{query} PSA+{grade}"
    print(f"Looking up PSA {grade}: {query}")
    averages = averageEbayPrices(query, country="uk")
    print(f"Average for {query} results={averages}")

    return averages
