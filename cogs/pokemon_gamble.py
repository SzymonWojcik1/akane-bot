from discord.ext import commands
import os
import json
import random
import discord
import asyncio

class PokemonPacks(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.base_set_file = "data/pokemon_sets_default/base_set.json"
        # Load the cards data from the JSON file
        with open(self.base_set_file, "r") as f:
            self.cards_data = json.load(f)["cards"]
        print(f"Loaded {len(self.cards_data)} cards from {self.base_set_file}")

    def draw_unique_card(self, rarity, drawn_cards):
        """
        Draw a unique card from a specific rarity
        Args:
            rarity (str): rarity of cards to pull
            drawn_cards (set): A set of cards already pulled to avoid duplicates
        Returns: dict or None: the card data dictionary or None if there are no available cards
        """
        # Filter cards by rarity and exclude already drawn cards
        available_cards = [
            card for card in self.cards_data
            if card['rarity'] == rarity and card['image'] not in drawn_cards
        ]

        print(f"Available cards for {rarity}: {len(available_cards)}")  # Debug statement

        # If there are available cards, return a random one
        if available_cards:
            return random.choice(available_cards)
        else:
            return None

    async def display_cards(self, ctx, pack_ids, rarities):
        """
        Opens the pack and shows the cards to the user with a discord message.
        It shows the image and name of the card while changing every 2 seconds to go on the next card.
        At the end, it shows every card drawn.
        Args:
            ctx (commands.Context): Execution context, can manipulate a discord message.
            pack_ids: A list of card data dictionaries to display.
            rarities: A list of rarities of the cards to display to the user.
        """
        display_message = await ctx.reply("🎁 **Ouverture du pack...** 🎉")
        await asyncio.sleep(2)

        card_info = []  # Stores formatted card names (for display only)
        pulled_cards = []  # Stores raw card names (for tracking purposes)
        rarity_colors = {
            "common": discord.Color.green(),
            "uncommon": discord.Color.blue(),
            "rare": discord.Color.purple(),
            "holo": discord.Color.gold()
        }

        # Loop through each card
        # Iterate through the combined lists of card IDs and their rarities,
        #   starting from index 1. On each iteration, 'i' gives the position
        #       of the card in the pack (1, 2, 3...), 'card_data' contains the
        #           card ID from the pack, and 'rarity' holds the card's rarity.
        for i, (card_data, rarity) in enumerate(zip(pack_ids, rarities), start=1):
            raw_card_name = card_data['name']
            pulled_cards.append(f"{raw_card_name} ({rarity})")

            formatted_card_name = raw_card_name.replace("_", " ").capitalize()
            card_info.append(f"{formatted_card_name} ({rarity})")

            img = card_data['image']
            print(f"Displaying {formatted_card_name} with image {img} id of the card : {card_data['id']}")  # Debug statement

            file = discord.File(img)

            embed = discord.Embed(
                title=f"📜 Carte {i}/{len(pack_ids)}",
                description=f"**Nom:** {formatted_card_name}\n**Rareté:** {rarity}",
                color=rarity_colors.get(rarity)
            )
            embed.set_image(url=f"attachment://{os.path.basename(img)}")

            await display_message.edit(content=None, embed=embed, attachments=[file])
            await asyncio.sleep(2)

        # Final new message with all drawn cards
        embed_final = discord.Embed(
            title="🎉 Pack Ouvert !",
            description="Voici les cartes que tu as obtenues :\n" + "\n".join(card_info),
            color=discord.Color.red()
        )
        # New message
        await ctx.reply(content=None, embed=embed_final)

    @commands.command()
    @commands.cooldown(1, 180, commands.BucketType.user)
    async def baseset(self, ctx):
        """
        Open a pack of cards with rarities distributed between common, uncommon, rare and holo.
        Displays the drawn cards and their rarities to the user.
        Args: ctx (commands.Context): The context of the command execution to reply in discord
        """
        pack_ids = []  # List to store the path of the drawn cards
        rarities = []  # List of rarities of the drawn cards
        drawn_cards = set()  # A set to track the cards already drawn

        # Draw 3 common cards
        for _ in range(3):
            card_data = self.draw_unique_card("common", drawn_cards)
            if card_data:
                pack_ids.append(card_data)
                rarities.append("common")
                drawn_cards.add(card_data['image'])  # Use image path to track duplicates

        # Draw 2 uncommons cards, or one common and one uncommon based on luck
        uncommon_chance = random.randint(1, 2)
        for _ in range(2):
            rarity = "uncommon" if uncommon_chance == 2 or len(pack_ids) == 4 else "common"
            card_data = self.draw_unique_card(rarity, drawn_cards)
            if card_data:
                pack_ids.append(card_data)
                rarities.append(rarity)
                drawn_cards.add(card_data['image'])  # Use image path to track duplicates

        # 1 in 3 chances to open a holo card instead of a rare one
        final_rarity = "holo" if random.randint(1, 3) == 1 else "rare"
        final_card_data = self.draw_unique_card(final_rarity, drawn_cards)
        if final_card_data:
            pack_ids.append(final_card_data)
            rarities.append(final_rarity)
            drawn_cards.add(final_card_data['image'])  # Use image path to track duplicates

        # Check if any cards were drawn, otherwise send an error message
        if not pack_ids:
            await ctx.reply("Aucune image trouvée.")
            return

        # Display the cards
        await self.display_cards(ctx, pack_ids, rarities)

    @baseset.error
    async def pokemon_error(self, ctx, error):
        """
        Function to send an error if a user tries to draw a card before a cooldown
        """
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"Tu dois attendre encore {round(error.retry_after, 1)} secondes avant de réessayer.")