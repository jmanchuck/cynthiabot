import os
from dotenv import load_dotenv
import requests


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
CYNTHIA_BOT_ID = os.getenv("CYNTHIA_BOT_ID")

url = (
    f"https://discord.com/api/v10/applications/{CYNTHIA_BOT_ID}/guilds/{GUILD}/commands"
)

# This is an example USER command, with a type of 2
json = {"name": "psa", "type": 2, "description": "/psa <grade> <query>"}

# For authorization, you can use either your bot token
headers = {"Authorization": f"Bot {TOKEN}"}

r = requests.post(url, headers=headers, json=json)
