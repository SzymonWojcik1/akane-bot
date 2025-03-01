from discord.ext import commands
import os
import random
import discord
import asyncio
from discord.ext.commands import CommandOnCooldown

class PokemonPacks(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Cooldown de 10 secondes par utilisateur
    @commands.command()
    @commands.cooldown(1, 180, commands.BucketType.user)
    async def pokemon(self, ctx):
        # Dossiers des cartes
        image_folders = {
            "common": "assets/pokemon_cartes/base_set/common",
            "uncommon": "assets/pokemon_cartes/base_set/uncommon",
            "rare": "assets/pokemon_cartes/base_set/rare",
            "holo": "assets/pokemon_cartes/base_set/holo"
        }

        # Charger les images disponibles
        available_images = {rarity: [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.jpg')]
                            for rarity, folder in image_folders.items()}

        # Fonction pour tirer une carte unique d'une rareté donnée
        def draw_unique_card(rarity, drawn_cards):
            images = [img for img in available_images.get(rarity, []) if img not in drawn_cards]
            return random.choice(images) if images else None

        # Tirage des cartes
        pack = []
        drawn_cards = set()

        # Tirer 3 cartes common uniques
        for _ in range(3):
            card = draw_unique_card("common", drawn_cards)
            if card:
                pack.append(card)
                drawn_cards.add(card)

        # Tirer 2 cartes uncommon ou une combinaison avec common
        if random.randint(1, 2) == 1:  # 1 chance sur 2 qu'une uncommon soit remplacée par une common
            card1 = draw_unique_card("common", drawn_cards)
            card2 = draw_unique_card("uncommon", drawn_cards)
        else:
            card1 = draw_unique_card("uncommon", drawn_cards)
            card2 = draw_unique_card("uncommon", drawn_cards)

        for card in [card1, card2]:
            if card:
                pack.append(card)
                drawn_cards.add(card)

        # Tirer une rare ou une holo (1 chance sur 3 pour une holo)
        if random.randint(1, 3) == 1:
            final_card = draw_unique_card("holo", drawn_cards)
        else:
            final_card = draw_unique_card("rare", drawn_cards)

        if final_card:
            pack.append(final_card)
            drawn_cards.add(final_card)

        # Vérifier si le pack contient des cartes
        if not pack:
            await ctx.reply("Aucune image trouvée.")
            return

        # Création du message initial
        display_message = await ctx.reply("🎁 **Ouverture du pack...** 🎉")
        await asyncio.sleep(2)  # Attendre 2 secondes avant de commencer l'affichage

        # Affichage des cartes une par une en modifiant le message
        for i, img in enumerate(pack, start=1):
            file = discord.File(img)
            await display_message.edit(content=f"📜 **Carte {i}/{len(pack)} :**", attachments=[file])
            await asyncio.sleep(2)  # Pause de 2 secondes entre chaque carte

        # Supprimer le message après 2 minutes
        await asyncio.sleep(120 - (2 * len(pack)))  # Ajuste le timer pour rester à 2 min au total
        try:
            await display_message.delete()
        except discord.NotFound:
            pass  # Ignore l'erreur si le message est déjà supprimé

    # Gestion des erreurs de cooldown
    @pokemon.error
    async def test_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.reply(f"Tu dois attendre encore {round(error.retry_after, 1)} secondes avant de réessayer.")