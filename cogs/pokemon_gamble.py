from discord.ext import commands
import os
import random
import discord
import asyncio

class PokemonPacks(commands.Cog):
    def __init__(self, client):
        self.client = client
        # Add futur sets here
        self.image_folders = {
            "common": "assets/pokemon_cartes/base_set/common",
            "uncommon": "assets/pokemon_cartes/base_set/uncommon",
            "rare": "assets/pokemon_cartes/base_set/rare",
            "holo": "assets/pokemon_cartes/base_set/holo"
        }
        self.available_images = self.load_images()

    def load_images(self):
        """
        Load images from the self.image_folder
        returns:
            dictionnary where rarity is the key
        """
        return {
            rarity: [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith('.jpg')]
            for rarity, folder in self.image_folders.items()
        }

    def draw_unique_card(self, rarity, drawn_cards):
        """
        Draw a unique card from a specific rarity
        Args:
            rarity (str): rarity of cards to pull
            draw_cards (set): A set of cards already pulled to avoid duplicates

        Returns:
            str or none: path to the drawn card or nothing if there is a problem
        """
        images = [img for img in self.available_images.get(rarity, []) if img not in drawn_cards]
        return random.choice(images) if images else None

    async def display_cards(self, ctx, pack, rarities):
        """
        Opens the pack and shows the cards to the user with a discord message
        It shows the image and name of the card while changing every 2 seconds to go on the next card
        at the end it shows every card drawn

        Args:
            ctx (commands.Context): execution context, can manipulate a discord message
            pack(list): A list of paths to the cards to print
            rarities (list): A list of the rarities of the cards to display to the user
        """
        display_message = await ctx.reply("🎁 **Ouverture du pack...** 🎉")
        await asyncio.sleep(2)

        card_info = []  # Pour stocker les informations sur les cartes (nom et rareté)

        for i, (img, rarity) in enumerate(zip(pack, rarities), start=1):
            # Extraire le nom de la carte depuis le fichier (sans l'extension .jpg)
            card_name = os.path.basename(img).replace(".jpg", "")
            card_info.append(f"{card_name} ({rarity})")

            file = discord.File(img)
            await display_message.edit(content=f"📜 **Carte {i}/{len(pack)} :** {card_name} ({rarity})", attachments=[file])
            await asyncio.sleep(2)

        # Ajouter un message avec les noms des cartes et leur rareté
        await display_message.edit(content=f"Voici les cartes que tu as obtenues :\n" + "\n".join(card_info))

        await asyncio.sleep(max(0, 120 - (2 * len(pack))))
        try:
            await display_message.delete()
        except discord.NotFound:
            pass

    @commands.command()
    @commands.cooldown(1, 180, commands.BucketType.user)
    async def baseset(self, ctx):
        """
        Open a pack cards with rarities ditributed between common, uncommon, rare and holo
        Displays the drawn cards and their rarities to the user
        Args :
            ctx (commands.Context): The context of the command execution to reply in discord
        """
        pack = [] # List to store the path of the drawn cards
        rarities = [] # List of rarities of the drawn cards
        drawn_cards = set() # A set to track the cards already drawn

        # Draw 3 common cards
        # Adds the card to the pack
        for _ in range(3):
            card = self.draw_unique_card("common", drawn_cards)
            if card:
                pack.append(card)
                rarities.append("common")
                drawn_cards.add(card)

        # Draw 2 uncommons cards, or one common et one uncommon based on luck
        # Adds the card the the pack as before
        uncommon_chance = random.randint(1, 2)
        for _ in range(2):
            rarity = "uncommon" if uncommon_chance == 2 or len(pack) == 4 else "common"
            card = self.draw_unique_card(rarity, drawn_cards)
            if card:
                pack.append(card)
                rarities.append(rarity)
                drawn_cards.add(card)

        # 1 in 3 chances to open a holo card instead of a rare one
        final_rarity = "holo" if random.randint(1, 3) == 1 else "rare"
        final_card = self.draw_unique_card(final_rarity, drawn_cards)
        if final_card:
            pack.append(final_card)
            rarities.append(final_rarity)
            drawn_cards.add(final_card)

        # Check if any cards were drawn, otherwise send an error message
        if not pack:
            await ctx.reply("Aucune image trouvée.")
            return

        await self.display_cards(ctx, pack, rarities)

    @baseset.error
    async def pokemon_error(self, ctx, error):
        """
        Function to send an error if a user tries to draw a card before a cooldown
        """
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"Tu dois attendre encore {round(error.retry_after, 1)} secondes avant de réessayer.")