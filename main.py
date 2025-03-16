import discord
from discord.ext import commands
from discord import app_commands
import json
import asyncio
from utils.file_utils import load_config
from cogs.pokemon_gamble import PokemonPacks
from cogs.help import Help
from utils.generate_json import generate_json_file



intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents, help_command=None) # help_command makes it possible to name my help -> help

# base set pokemon
base_set_rarities = ["common", "uncommon", "rare", "holo"]
base_set_output_file = "data/pokemon_sets_default/base_set.json"
base_set_path = "assets/pokemon_cartes/base_set"


@client.event
async def on_ready():
    """
    On start up, changes the message under the bot name to diplay "!help..."
    """
    activity = discord.Game(name="!help pour voir les commandes")
    await client.change_presence(activity=activity)
    print(f"{client.user} est connecté !")

    generate_json_file(base_set_output_file, base_set_path, base_set_rarities)

    await client.tree.sync()


async def main():
    # loads the config.json
    config = load_config()
    discord_token = config.get('discord_bot_token') # Get the token "discord_bot_token"

    # Loads the pokemon_gamble.py commands and help.py
    await client.add_cog(PokemonPacks(client))
    await client.add_cog(Help(client))

    await client.start(discord_token)

# Start the app
asyncio.run(main())