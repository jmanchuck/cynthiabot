import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import Colour, Embed, Intents
from cynthiabot_processor import psa_ebay_average

from src.ebay.completed import Average
from src.ebay.scrape import find
from src.tcgrepublic.scrape import get_html, parse_items

from currency_converter import CurrencyConverter

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

intents = Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

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


@bot.command()
async def query(ctx, *args):
    print(f"Query arguments: {', '.join(args)}")


@bot.command(name="psa")
async def _psa_lookup(ctx, grade: int, *args):
    print(f"Looking up PSA {grade} for card {' '.join(args)}")

    # Put "" around each word to force
    query = " ".join([f'"{a}"' for a in args]) + f" PSA+{grade}"

    averages = Average(query, country="uk")

    embed = Embed(title=query, colour=Colour.teal(), url=averages["url"])

    embed.add_field(name=f"Average Sold", value=f"{averages['total']} GBP")
    embed.add_field(name=f"Number of items", value=averages["count"])

    await ctx.send(embed=embed)


@bot.command(name="ebay")
async def _ebay_lookup(ctx, *args):
    print(f"Looking for card {' '.join(args)}")

    query = " ".join([f'"{a}"' for a in args])

    result, search_url = find(query)

    print(search_url)

    if len(result) == 0:
        await ctx.send("ERROR COULD NOT FIND LISTINGS")
        return

    price_list = [
        float(row["sellingStatus"]["convertedCurrentPrice"]["value"]) for row in result
    ]

    average = CurrencyConverter.convert(sum(price_list) / len(result), "USD", "GBP")

    embed = Embed(title=" ".join(args), colour=Colour.gold(), url=search_url)

    embed.set_image(url=result[0]["galleryURL"])

    embed.add_field(name="Min/Max", value=f"{min(price_list)} / {max(price_list)}")
    embed.add_field(name="Average", value=f"${average:.2f}")

    await ctx.send(embed=embed)


@bot.command(name="tcgrepublic")
async def _tcgrepublic(ctx, url: str):
    print(f"Analysing prices on tcgrepublic link: {url}")

    items = parse_items(get_html(url))

    highlights = []

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

        psa10_averages = psa_ebay_average(query, 10)
        embed.add_field(
            name="PSA 10 Average Sold",
            value=f"[£{psa10_averages['total']}]({psa10_averages['url']})"
            if psa10_averages["count"] != 0
            else "N/A",
        )

        if psa10_averages["total"] > average or psa9_averages["total"] > average:
            highlights.append(
                f"{display_query}, Average: {average}, PSA 9 {psa9_averages['total']}, PSA 10 {psa10_averages['total']}"
            )
            embed.colour = Colour.green()

            await ctx.send(embed=embed)

        elif psa10_averages["total"] > min(price_list):
            await ctx.send(embed=embed)

    highlights_summary = "\n".join(highlights)
    await ctx.send(f"Highlights: {highlights_summary}")


# bot.loop.create_task()
def start():
    bot.run(TOKEN)
