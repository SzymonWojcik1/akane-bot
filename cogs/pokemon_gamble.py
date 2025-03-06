from discord.ext import commands
import os
import random
import discord
import asyncio
from discord.ext.commands import CommandOnCooldown

class PokemonPacks(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 180, commands.BucketType.user)
    async def baseset(self, ctx):

        await ctx.reply("Test")
    # Gestion des erreurs de cooldown
    @baseset.error
    async def test_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.reply(f"Tu dois attendre encore {round(error.retry_after, 1)} secondes avant de réessayer.")