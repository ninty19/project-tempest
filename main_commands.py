import discord
from discord.ext import commands
import json,ollama
import random, asyncio, time, os
asyncllm=ollama.AsyncClient()
llm=ollama.Client()
import memory as m
import tts
file="memory.json"
with open("config.json") as f: #opens config file and loads into memory
    cfg=json.load(f)

class main(commands.Cog):


    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def forget(self, ctx):
        memory_filename="memory.json"
        await ctx.send("wait wha-")
        with open(memory_filename, "w") as f:
            json.dump([], f)

        await ctx.send("https://tenor.com/view/fade-away-oooooooooooo-aga-emoji-crumble-gif-20008708")
        await ctx.send("hello my name is tempest how may i assist you today")



    @commands.command()
    async def annoy(self,ctx, n: int):
        with open("config.json") as f:
            cfg=json.load(f)
        if n <= 20 and ctx.channel.id in cfg["permitted_channels"]:
            for i in range(n):
                choice = random.choice(cfg["gifs"])
                await ctx.send(choice)
        else:
            return
    @commands.command()
    @commands.is_owner()
    async def dm(self, ctx, user: discord.User, *, message: str):
        await ctx.send(f"roger sending {message}")
        await user.send(message)

    @commands.command()
    @commands.is_owner()
    async def auto_shutdown(self, cxt, delay_seconds: int):
        await cxt.send(f"shutdown program in{delay_seconds}s")
        await asyncio.sleep(delay_seconds)
        print("Timed shutdown triggered.")
        await self.bot.close()  # Gracefully closes the bot
        os.system("shutdown /s /t 0")  # Linux / Pi shutdown command

    @commands.command()
    async def join(self,ctx):
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel
            vc = ctx.guild.voice_client# get vc
            try:
                if vc is None: #check vc
                    await channel.connect()
                    await ctx.send(f"Joined {channel.name}!")
                elif vc.channel != channel:
                    await vc.disconnect()
                    await channel.connect()
                    await ctx.send(f"Moved to {channel.name}!")
                else:
                    await ctx.send("Already connected here!")
            except NameError as e:
                print(f"The error is {e}")

        else:
            await ctx.send("You must be in a voice channel!") #error handling

    @commands.command()
    async def leave(self,ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("👋 Left the voice channel.")
        else:
            await ctx.send("❌ I'm not in a voice channel.")


    @commands.command()
    async def story(self, ctx):
        with open("story.txt", "r", encoding="utf-8") as f: #open story.txt file
            story = f.read()

        await tts.speak(ctx.guild, ctx.channel, story)#read out loud


def setup(bot):
    bot.add_cog(main(bot))