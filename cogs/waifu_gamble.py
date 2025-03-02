import requests
import json
import discord
from discord.ext import commands
from discord.ext.commands import CommandOnCooldown
from utils.file_utils import load_config, load_data, join_user
import asyncio

class Waifu(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def joinwaifu(self, ctx):
        waifu_file = 'users_waifus.json'

        users_waifu = load_data(waifu_file)
        user = str(ctx.author)
        success = join_user(user, users_waifu, waifu_file)

        if success :
            await ctx.reply(f"{ctx.author.name}, vous avez été ajouté à la base de données des waifus")
        else:
            await ctx.reply(f"{ctx.author.name}, vous êtes déjà dans la base de données des waifus")

    @commands.command()
    @commands.cooldown(1, 180, commands.BucketType.user)
    async def waifu(self, ctx):
        # Charger les données des waifus
        users_waifus = load_data('users_waifus.json')

        # Vérifier si l'utilisateur est dans la base de données
        user_id = str(ctx.author)
        if user_id not in users_waifus:
            await ctx.reply(f"{ctx.author.name}, tu n'es pas encore dans la base de données des waifus. Utilise `!joinwaifu` pour rejoindre !")
            return

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

            embed = discord.Embed(title=name_full, description=f"De : {title_romaji}", color=discord.Color.pink())
            embed.set_image(url=image_url)

            message = await ctx.reply(embed=embed)

            # Créer le message à envoyer
            await message.add_reaction("💖")
            await message.add_reaction("❌")

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["💖","❌"]

            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=60.0, check=check)

                if str(reaction.emoji) == "💖":
                    await ctx.send(f"{ctx.author.name} test")
                    await message.clear_reactions()
                    pass
                elif str(reaction.emoji) == "❌":
                    await ctx.send(f"Pass")
                    await message.clear_reactions()
                    pass


            except asyncio.TimeoutError:
                await message.clear_reactions()
                pass  # Ne rien faire si personne ne réagit

        else:
            await ctx.reply(f"Erreur lors de la récupération de la waifu. Code : {response.status_code}")


            # Répondre au message d'origine de l'utilisateur (ctx.reply)
            await ctx.reply(message)

    @waifu.error
    async def waifu_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            # Si la commande est en cooldown, envoie un message indiquant le temps restant
            time_left = round(error.retry_after)
            await ctx.reply(f"Tu dois attendre {time_left} secondes avant de pouvoir utiliser cette commande à nouveau.")
        else:
            # Si une autre erreur survient, l'afficher
            await ctx.reply(f"Une erreur est survenue : {str(error)}")