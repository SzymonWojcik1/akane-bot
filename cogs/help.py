from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command()
    async def help(self, ctx):
        """
        When the user types !help, it provides a list of commands while explaining what they do

        Args:
            ctx : context command, used here to reply to the user with a discord message
        """
        help_message = (
            "**Commandes disponibles :**\n\n"
            "**!help** : Affiche les commandes du bot\n\n"
            "**!verison** : Affiche la version du bot\n\n"
            "**!baseset** : Ouvre un pack Pokémon du set de base.\n"
            "Utilisez cette commande pour ouvrir un pack Pokemon.\n\n"
            "Chaque commande est disponible avec un délai de 180 secondes entre les utilisations (cooldown)."
        )
        await ctx.reply(help_message)

    @commands.command()
    async def version(self, ctx):
        version = "1.1.0"
        await ctx.reply(f"Version du bot : {version}")