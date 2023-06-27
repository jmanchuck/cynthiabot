from src.ebay.completed import Average


def psa_ebay_average(query: str, grade: int):
    query = f"{query} PSA+{grade}"
    print(f"Looking up PSA 9: {query}")
    averages = Average(query, country="uk")
    print(f"Average for {query} results={averages}")

    return averages
