import discord
from discord.ext import commands
import json
import asyncio

# Charger la configuration (token) depuis le fichier config.json
def load_config(filename='config.json'):
    try:
        with open(filename, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to parse {filename} as JSON.")
        return None

# Créer un client Discord avec le préfixe de commande
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

# Ajouter le Cog à partir du fichier séparé
async def main():
    config = load_config()
    discord_token = config.get('discord_bot_token')

    # Ajouter le Cog contenant la commande test
    from cogs.test_cog import TestCog
    await client.add_cog(TestCog(client))

    await client.start(discord_token)

# Lancer le bot avec asyncio
asyncio.run(main())