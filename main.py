import discord
from discord.ext import commands
import json
import asyncio
from utils.file_utils import load_config
from cogs.pokemon_gamble import PokemonPacks
from cogs.help import Help



intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@client.event
async def on_ready():
    activity = discord.Game(name="!help pour de l'aide")
    await client.change_presence(activity=activity)
    print(f"{client.user} est connecté !")


async def main():
    config = load_config()
    discord_token = config.get('discord_bot_token')

    await client.add_cog(PokemonPacks(client))
    await client.add_cog(Help(client))

    await client.start(discord_token)

# Lancer le bot avec asyncio
asyncio.run(main())