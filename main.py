import discord
from discord.ext import commands
import json
import asyncio
from utils.config_loader import load_config
from cogs.waifu_gamble import TestWaifu
from cogs.pokemon_gamble import TestCog



intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

async def main():
    config = load_config()
    discord_token = config.get('discord_bot_token')

    await client.add_cog(TestCog(client))
    await client.add_cog(TestWaifu(client))

    await client.start(discord_token)

# Lancer le bot avec asyncio
asyncio.run(main())