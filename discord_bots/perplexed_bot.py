import discord
from model.model import *
from utils.reddit import Reddit

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
model = Model()
reddit = Reddit()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('/question'):
        try:
            question = message.content.split('/question ')[1]
            processing_msg = await message.channel.send("Processing your question...")
            response = model.generate(question)
            await processing_msg.edit(content=response)
        except Exception as e:
            await message.channel.send("Some error occurred, unable to process...", e)
    
    if message.content.startswith("/search"):
        try:
            question = message.content.split('/search ')[1].strip()
            processing_msg = await message.channel.send("Processing your search...")
            response = reddit.get_subreddit_urls(question)
            await processing_msg.edit(content=response)
        except Exception as e:
            await message.channel.send("Some error occurred, unable to process...", e)