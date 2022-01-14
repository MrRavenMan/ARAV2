import asyncio
import time
import configparser

import discord 
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.ext.commands import Cog

from youtube_dl import YoutubeDL



config = configparser.ConfigParser()
config.read("conf/config.ini")


class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.song_queue = []


    @Cog.listener()
    async def on_ready(self):
        print("Music Player: ON")


    async def check_queue(self, ctx):
        if len(self.song_queue) > 0:
            ctx.voice_client.stop()
            await self.play_song(ctx, self.song_queue[0])
            self.song_queue.pop(0)


    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: YoutubeDL({"format": "bestaudio", "quiet": True})
            .extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0: 
            return None
        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info


    async def play_song(self, ctx, song):
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        voice = ctx.voice_client
        ydl_opts = {
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'song.%(ext)s',
        }

        if not voice.is_playing():
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(song, download=False)
            URL = info['formats'][0]['url']
            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            voice.is_playing()
        else:
            await ctx.send("Already playing song")
            return
        #url = pafy.new(song).getbestaudio().url
        #ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=lambda error: self.bot.loop.create_task(self.check_queue, ctx))
        #ctx.voice_client.source.volume = 0.5

    async def react(self, ctx):
        await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
        time.sleep(0.5)
        await ctx.message.delete()



    """ Music Player Commands """
    @commands.has_role(int(config["MusicPlayer"]["music_player_admin_role_id"]))
    @commands.command(brief="Force bot to join a voice channel *DEPRECATED!")
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send("You are not connected to a voice channel. I ain't playing nothing without you!")

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()
        
        await self.react(ctx)


    @commands.has_role(int(config["MusicPlayer"]["music_player_admin_role_id"]))
    @commands.command(brief="Force bot to leave a voice channel *DEPRECATED!")
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()

        await ctx.send("I am not connected to a voice channel")

        await self.react(ctx)


    @commands.has_role(int(config["MusicPlayer"]["music_player_role_id"]))
    @commands.command(brief="!play [songname] or !play [youtube url] - make bot play song in your currenct voice channel")
    async def play(self, ctx, *, song=None):
        if song is None:
            if len(self.song_queue) != 0:
                await self.check_queue(ctx)
            else:
                return await ctx.send("You must include a song to play")
        
        if ctx.voice_client is None:
            try:
                await ctx.author.voice.channel.connect()
            except:
                return await ctx.send("I must be in a voice channel to play a song")

        #handle a song where song isn't url
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send(f"Searching for ***{song}***, this may take a few moments")
            
            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send("Ay, I cannot find the given song. Try using my search command!")

            song = result[0]


        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue)

            if queue_len < int(config["MusicPlayer"]["max_queue_amount"]):
                self.song_queue.append(song)
                return await ctx.send(f"I am currently playing a song. This song is number {queue_len + 1} in queue")

            else:
                return await ctx.send(f"Sorry, I can only queue up to {int(config['MusicPlayer']['max_queue_amount'])} songs!")

        await self.play_song(ctx, song)
        await ctx.send(f"Now playing: {song}")

        await self.react(ctx)


    @commands.has_role(int(config["MusicPlayer"]["music_player_role_id"]))
    @commands.command(brief="display current queued songs")
    async def queue(self, ctx):
        if len(self.song_queue) == 0:
            return await ctx.send("There is currently no songs in the queue")

        embed = discord.Embed(title="Song Queue", description="", colour=discord.Colour.dark_gold())
        i = 1
        for url in self.song_queue:
            embed.description += f"{i}) {url}\n"

            i += 1
            
        embed.set_footer(text="")
        await ctx.send(embed=embed)

        await self.react(ctx)


    @commands.has_role(int(config["MusicPlayer"]["music_player_admin_role_id"]))
    @commands.command(brief="Wipe song queue")
    async def wipe_queue(self, ctx):
        self.song_queue = []

        await self.react(ctx)


    @commands.has_role(int(config["MusicPlayer"]["music_player_role_id"]))
    @commands.command(brief="Pause song")
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Music is now paused")
        else:
            await ctx.send("I am not playing anything at the moment")

        await self.react(ctx)


    @commands.has_role(int(config["MusicPlayer"]["music_player_role_id"]))
    @commands.command(brief="Resume paused song")
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
        else:
            await ctx.send("I am not paused!")

        await self.react(ctx)


    @commands.has_role(int(config["MusicPlayer"]["music_player_role_id"]))
    @commands.command(brief="Stop song (Also wipes song queue)")
    async def stop(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        #else:
            #await ctx.send("I am not playing anything at the moment")

        self.song_queue = []
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()

        await self.react(ctx)
        

    @commands.has_role(int(config["MusicPlayer"]["music_player_admin_role_id"]))
    @commands.command(brief="Skip song to next song in queue")
    async def skip(self, ctx):
        ctx.voice_client.stop()
        await self.check_queue(ctx)

        await self.react(ctx)

    @commands.has_role(int(config["MusicPlayer"]["music_player_role_id"]))
    @commands.command(brief="Start vote on skip song")
    async def next(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not playing any song")

        if ctx.author.voice is None:
            return await ctx.send("You are not connected to any voice channel")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("I am not currently playing any songs for you")

        poll = discord.Embed(title=f"Vote to skip song by - {ctx.author.name}#{ctx.author.discriminator}", description="**80% of the voice channel must vote to skip song")
        poll.add_field(name="Skip", value=":white_check_mark:")
        poll.add_field(name="Stay", value=":no_entry_sign:")
        poll.set_footer(text="Voting ends in 15 seconds")

        poll_msg = await ctx.send(embed=poll) # Only returns temporary message, we need to get the cached message to get reactions
        poll_id = poll_msg.id
        
        await poll_msg.add_reaction(u"\u2705") # yes
        await poll_msg.add_reaction(u"\U0001F6AB") # no

        await asyncio.sleep(15) # 15 seconds to vote

        poll_msg = await ctx.channel.fetch_message(poll_id)

        votes = {u"\u2705": 0, u"\U0001F6AB": 0}
        reacted = []

        for reaction in poll_msg.reactions:
            if reaction.emoji in [u"\u2705", u"\U0001F6AB"]:
                async for user in reaction.users():
                    if user.voice.channel.id == ctx.voice_client.channel.id and user.id not in reacted and not user.bot:
                        votes[reaction.emoji] += 1

                        reacted.append(user.id)
        
        skip = False

        if votes[u"\u2705"] > 0:
            if votes[u"\U0001F6AB"] == 0 or votes[u"\u2705"] / (votes[u"\u2705"] + votes[u"\U0001F6AB"]) > 0.79: # 80% or higher has votes skip
                skip = True
                embed = discord.Embed(title="Skip succesful", description="***Voting to skip current song was succesful, skipping now.***")

        if not skip:
            embed = discord.Embed(title="Skip failed", description="*Voting to skip current song has failed.* \n\n Vote requires 80 pct or more to vote skip")

        embed.set_footer(text="Voting has ended")

        await poll_msg.clear_reactions()
        await poll_msg.edit(embed=embed)

        if skip:
            ctx.voice_client.stop()
            await self.check_queue(ctx)