from typing import List, Tuple
from discord import Colour, Embed, SyncWebhook

CYNTHIA_DEAL_GENERAL = "https://discord.com/api/webhooks/1118674007684808805/Agm6cny2LDfkwjjrAjvYS-NwrRzesZ-K4PSqEOSiZuCohOjB6u8mW8DGA3-FKKLlDyIJ"


def send_embedded_message(
    title: str,
    url: str,
    description: str = "",
    image_url: str = None,
    fields: List[Tuple[str, str]] = None,
):
    print(f"Args to function: {list(locals().items())}")
    embed = Embed(title=title, colour=Colour.teal(), url=url, description=description)
    if image_url:
        embed.set_image(url=image_url)

    for field in fields:
        embed.add_field(name=field[0], value=field[1])

    SyncWebhook.from_url(CYNTHIA_DEAL_GENERAL).send(embed=embed)


def send_message(text: str):
    SyncWebhook.from_url(CYNTHIA_DEAL_GENERAL).send(text)


if __name__ == "__main__":
    send_message("Good night!")
