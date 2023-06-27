import os
from dotenv import load_dotenv
import discord
from discord import Colour, Embed, Intents, Option

from src.cynthiabot_processor import psa_ebay_average
from src.ebay.completed import Average
from src.ebay.scrape import find
from src.tcgrepublic.scrape import get_html, parse_items

from currency_converter import CurrencyConverter

import logging

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

load_dotenv()
TOKEN = str(os.getenv("TOKEN"))
GUILD = os.getenv("DISCORD_GUILD")

intents = Intents.default()
intents.messages = True
intents.message_content = True

# bot = commands.Bot(command_prefix="/", intents=intents)

bot = discord.Bot(intents=intents)

cynthia_general = 1118633292963528737


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    channel = bot.get_channel(cynthia_general)
    if channel:
        await channel.send("I'm ready, let's get started!")
    else:
        print(f"Channel with ID {cynthia_general} not found.")
        await bot.close()


@bot.event
async def on_disconnect():
    channel = bot.get_channel(cynthia_general)
    if channel:
        await channel.send("I'm logging off, bye!👋👋")
    else:
        print(f"Channel with ID {cynthia_general} not found.")


@bot.slash_command(
    name="psa",
    description="Search PSA solds",
    options=[
        Option(name="grade", description="PSA grade"),
        Option(name="query", description="Search string"),
    ],
)
async def psa(ctx, grade: int, query):
    print(f"Looking up PSA {grade} for card {query}")

    # Put "" around each word to force
    ebay_query = " ".join([f'"{a}"' for a in query.split(" ")]) + f" PSA+{grade}"

    averages = Average(ebay_query, country="uk")

    embed = Embed(title=query, colour=Colour.teal(), url=averages["url"])

    embed.add_field(name=f"Average Sold", value=f"{averages['total']} GBP")
    embed.add_field(name=f"Number of items", value=averages["count"])

    await ctx.respond(embed=embed)


@bot.slash_command(
    name="ebay",
    description="Search eBay listings",
    options=[Option(name="query", description="Search string")],
)
async def _ebay_lookup(ctx, query):
    print(f"Looking for card {query}")

    ebay_query = " ".join([f'"{a}"' for a in query.split(" ")])

    result, search_url = find(ebay_query)

    print(search_url)

    if len(result) == 0:
        await ctx.send("ERROR COULD NOT FIND LISTINGS")
        return

    price_list = [
        float(row["sellingStatus"]["convertedCurrentPrice"]["value"]) for row in result
    ]

    average = CurrencyConverter.convert(sum(price_list) / len(result), "USD", "GBP")

    embed = Embed(title=query, colour=Colour.gold(), url=search_url)

    embed.set_image(url=result[0]["galleryURL"])

    embed.add_field(name="Min/Max", value=f"{min(price_list)} / {max(price_list)}")
    embed.add_field(name="Average", value=f"${average:.2f}")

    await ctx.send(embed=embed)


@bot.slash_command(
    name="delta",
    description="Searches PSA 9, PSA 10 solds and current eBay listings given a query",
    options=[Option(name="query", description="Search string")],
)
async def delta(ctx, query: str):
    ebay_query = " ".join([f'"{a}"' for a in query.split(" ")])

    result, search_url = find(query, include_auction=False)

    if len(result) == 0:
        await ctx.send(f"Couldn't find listings for {query} 😞")
        return

    price_list = [
        float(row["sellingStatus"]["convertedCurrentPrice"]["value"]) for row in result
    ]

    average = sum(price_list) / len(result)

    embed = Embed(title=f"{query}", colour=Colour.teal(), url=search_url)

    embed.set_image(url=result[0]["galleryURL"])

    embed.add_field(name="Min/Max", value=f"{min(price_list)} / {max(price_list)}")
    embed.add_field(name="Average", value=f"£{average:.2f}")

    # PSA sold lookup

    psa9_averages = psa_ebay_average(query, 9)
    embed.add_field(
        name="PSA 9 Average Sold",
        value=f"[£{psa9_averages['total']}]({psa9_averages['url']})"
        if psa9_averages["count"] != 0
        else "N/A",
    )
    embed.add_field(name="PSA 9 Sold Count", value=psa9_averages["count"])

    psa10_averages = psa_ebay_average(query, 10)
    embed.add_field(
        name="PSA 10 Average Sold",
        value=f"[£{psa10_averages['total']}]({psa10_averages['url']})"
        if psa10_averages["count"] != 0
        else "N/A",
    )
    embed.add_field(name="PSA 10 Sold Count", value=psa10_averages["count"])

    await ctx.send(embed=embed)


@bot.slash_command(
    name="tcgrepublic",
    description="Pulls all cards from tcgrepublic page then searches PSA 9 solds, PSA 10 solds and eBay listings",
    options=[
        Option(name="url", description="tcgrepublic link"),
    ],
)
async def tcgrepublic(ctx, url: str):
    print(f"Analysing prices on tcgrepublic link: {url}")

    items = parse_items(get_html(url))

    for name, number in items:
        query = f'"{name}" "{number}"'
        display_query = f"{name} {number}"
        result, search_url = find(query, include_auction=False)

        if len(result) == 0:
            await ctx.send(f"Couldn't find listings for {display_query} 😞")
            continue

        price_list = [
            float(row["sellingStatus"]["convertedCurrentPrice"]["value"])
            for row in result
        ]

        average = sum(price_list) / len(result)

        embed = Embed(title=f"{display_query}", colour=Colour.orange(), url=search_url)

        embed.set_image(url=result[0]["galleryURL"])

        embed.add_field(name="Min/Max", value=f"{min(price_list)} / {max(price_list)}")
        embed.add_field(name="Average", value=f"£{average:.2f}")

        # PSA sold lookup

        psa9_averages = psa_ebay_average(query, 9)
        embed.add_field(
            name="PSA 9 Average Sold",
            value=f"[£{psa9_averages['total']}]({psa9_averages['url']})"
            if psa9_averages["count"] != 0
            else "N/A",
        )
        embed.add_field(name="PSA 9 Sold Count", value=psa9_averages["count"])

        psa10_averages = psa_ebay_average(query, 10)
        embed.add_field(
            name="PSA 10 Average Sold",
            value=f"[£{psa10_averages['total']}]({psa10_averages['url']})"
            if psa10_averages["count"] != 0
            else "N/A",
        )
        embed.add_field(name="PSA 10 Sold Count", value=psa10_averages["count"])

        if psa10_averages["total"] > average or psa9_averages["total"] > average:
            embed.colour = Colour.green()
            await ctx.send(embed=embed)


def start():
    bot.run(TOKEN)
