import discord
from discord.ext import commands
import yt_dlp
import asyncio
import json


intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

FFMPEG_OPTIONS = {'options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': True}

class AkaneBot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = []
        self.disconnect_timer = None

    @commands.command()
    async def play(self, ctx, *, search):
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if not voice_channel:
            return await ctx.send("Il faut être dans un channel !")
        if not ctx.voice_client:
            await voice_channel.connect()

        async with ctx.typing():
            try:
                with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(f"ytsearch:{search}", download=False)
                    if 'entries' in info:
                        info = info['entries'][0]
                    url = info['url']
                    title = info['title']
                    self.queue.append((url, title))
                    await ctx.send(f'Ajouter à la file : **{title}**')

                    # Cancel the auto-disconnect timer since there's a new song in the queue
                    if self.disconnect_timer:
                        self.disconnect_timer.cancel()
                        self.disconnect_timer = None

            except Exception as e:
                return await ctx.send(f"An error occurred: {str(e)}")

        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)

    async def play_next(self, ctx):
        if self.queue:
            url, title = self.queue.pop(0)
            try:
                source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
                ctx.voice_client.play(source, after=lambda _: self.client.loop.create_task(self.play_next(ctx)))
                await ctx.send(f'Joue actuellement **{title}**')
            except Exception as e:
                await ctx.send(f"An error occurred while trying to play: {str(e)}")
        elif not ctx.voice_client.is_playing():
            await ctx.send("La file est vide !")
            if not self.disconnect_timer:
                self.disconnect_timer = self.client.loop.create_task(self.auto_disconnect(ctx))

    async def auto_disconnect(self, ctx):
        await asyncio.sleep(60)
        if not self.queue and ctx.voice_client and ctx.voice_client.is_connected():
            await ctx.voice_client.disconnect()
            await ctx.send("Déconnecté du channel vocal car la file est restée vide.")

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send('Passage au morceau suivant !')

    @commands.command()
    async def file(self, ctx):
        if not self.queue:
            return await ctx.send("La file est vide !")

        queue_list = "\n".join(f"{index + 1}. {title}" for index, (_, title) in enumerate(self.queue))
        await ctx.send(f"**File actuelle :**\n{queue_list}")

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_connected():
            self.queue.clear()
            await ctx.voice_client.disconnect()
            await ctx.send("Déconnecté du channel vocal.")
            if self.disconnect_timer:
                self.disconnect_timer.cancel()
                self.disconnect_timer = None

client = commands.Bot(command_prefix="!", intents=intents)

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

async def main():
    # Load configuration from config.json
    config = load_config()

    discord_token = config.get('discord_bot_token')

    async with client:
        await client.add_cog(AkaneBot(client))
        await client.start(discord_token)

asyncio.run(main())
