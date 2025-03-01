from discord.ext import commands

class TestCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def test(self, ctx):
        # Hello World
        await ctx.send("Hello, World!")