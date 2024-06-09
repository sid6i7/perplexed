import os

from dotenv import load_dotenv
from discord_bots.perplexed_bot import client

if __name__ == "__main__":
    client.run(os.environ['DISCORD_BOT_TOKEN'])
