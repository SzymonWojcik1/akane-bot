import requests
import json
from discord.ext import commands
from discord.ext.commands import CommandOnCooldown
from utils.config_loader import load_config

class Waifu(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 180, commands.BucketType.user)
    async def waifu(self, ctx):
        # Charger les tokens depuis config.json
        config = load_config()
        waifu_token = config.get('waifu_token')

        # URL de l'API Waifu
        url = "https://waifu.it/api/v4/waifu"

        # Faire la requête avec le token Waifu
        response = requests.get(url, headers={
            "Authorization": waifu_token,
        })

        if response.status_code == 200:
            data = response.json()

            # Extraire les informations souhaitées
            name_full = data.get('name', {}).get('full', 'Nom non disponible')
            image_url = data.get('image', {}).get('large', 'Image non disponible')
            title_romaji = data.get('media', {}).get('nodes', [{}])[0].get('title', {}).get('romaji', 'Titre romaji non disponible')

            # Créer le message à envoyer
            message = f"**Nom complet :** {name_full}\n" \
                      f"**Image :** [Clique ici pour voir l'image]({image_url})\n" \
                      f"**Titre (Romaji) :** {title_romaji}"

            # Répondre au message d'origine de l'utilisateur (ctx.reply)
            await ctx.reply(message)

        else:
            await ctx.reply(f"Erreur lors de la récupération de la waifu. Code : {response.status_code}")

    @waifu.error
    async def waifu_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            # Si la commande est en cooldown, envoie un message indiquant le temps restant
            time_left = round(error.retry_after)
            await ctx.reply(f"Tu dois attendre {time_left} secondes avant de pouvoir utiliser cette commande à nouveau.")
        else:
            # Si une autre erreur survient, l'afficher
            await ctx.reply(f"Une erreur est survenue : {str(error)}")
