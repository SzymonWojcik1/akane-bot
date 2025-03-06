from discord.ext import commands
from discord.ext.commands import CommandOnCooldown

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        help_message = (
            "**Commandes disponibles :**\n\n"
            "**!pokemon** : Ouvre un pack Pokémon.\n"
            "Utilisez cette commande pour ouvrir un pack Pokemon.\n\n"
            "Chaque commande est disponible avec un délai de 180 secondes entre les utilisations (cooldown)."
        )
        await ctx.reply(help_message)