import discord
from discord.ext import commands
import json
import asyncio
from utils.file_utils import load_config
from cogs.waifu_gamble import Waifu
from cogs.pokemon_gamble import PokemonPacks



intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

async def main():
    config = load_config()
    discord_token = config.get('discord_bot_token')

    await client.add_cog(PokemonPacks(client))
    await client.add_cog(Waifu(client))

    await client.start(discord_token)

# Lancer le bot avec asyncio
asyncio.run(main())