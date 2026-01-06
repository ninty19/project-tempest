import discord
from discord.ext import commands
import logging
import ollama
import json

from sympy.physics.units import temperature

import memory
import vision
import tts
import ollama

#config
with open("config.json") as f: #opens config file and loads into memory
    cfg=json.load(f)

token= cfg["discord_token"]  #set up intents, log handler, ollama and memory
handler= logging.FileHandler(filename="tmps.log",encoding="utf-8",mode="w")
intents= discord.Intents.default()
intents.message_content=True
intents.members=True
intents.voice_states=True
llm=ollama.Client()
chat_model=cfg["chat_model"]
voice_model=cfg["voice_model"]
Bot=commands.Bot(command_prefix="//",intents=intents)
memory_filename="memory.json"
max_memory=cfg["memory_max_size"]
for ext in ("main_commands", "nfc_commands"):
    Bot.load_extension(ext)


#on ready event
@Bot.event
async def on_ready():
    await Bot.user.edit(username="//T.E.M.P.E.S.T experimental")
    print("startup")
    channel = Bot.get_channel(cfg["startup_channel"])
    await channel.send("all systems online\nhello! <3")



@Bot.event
async def on_member_join(member):
    server = str(member.guild.id)
    channel = Bot.get_channel(cfg["welcome"][server])
    await channel.send(f"{member.mention} hi welcome to the nfc. have fun")

@Bot.event
async def on_message(message, ):
    if message.author == Bot.user:
        return

    if Bot.user in message.mentions and message.channel.id in cfg["permitted_channels"]:
        print(f"{message.author} in {message.guild}#{message.channel} said: {message.content}")

        async with message.channel.typing():
            if message.guild.voice_client:
                model = voice_model
            else:
                model = chat_model

            memory.save(memory_filename, "user", f"{message.author.display_name}:{message.content}", max_memory)
            history = memory.load(memory_filename)
            print(f"this is the current history:\n{history}")

            if not history or history[0] == "error":
                await message.channel.send(f"someone tell {cfg['owner']} something is wrong with `{history[1] if history else 'memory'}`")
            else:
                if message.attachments or message.embeds:
                    image_url = (
                        message.attachments[0].url
                        if message.attachments
                        else message.embeds[0].image.url
                    )
                    response = await vision.generate(history, message.content, image_url,cfg["owner"])
                    if response != 0:
                        response=response["message"]["content"]
                        memory.save(memory_filename, "assistant", response, max_memory)
                    else:
                        await message.channel.send(f"someone tell {cfg['owner']} something is wrong with vision")

                else:
                    print(f"the one sending the message is: {message.author.display_name}")
                    history.append({
                        "role": "user",
                        "content": f"{message.author.display_name}: {message.content}"})
                    prompt = history
                    response = llm.chat(
                        model=model,
                        messages=prompt,
                        keep_alive=cfg["keep_alive"],
                        options={
                            "temperature": cfg["temp"],
                            "num_predict": 625,
                            "num_gpu": cfg["num_gpu"]
                        }
                    )

                    print(f"Response from llm {response.message.content}")
                    response=response["message"]["content"]
                    memory.save(memory_filename, "assistant", response, max_memory)

                await message.channel.send(response)

            if message.author.voice and message.author.voice.channel:
                vc = message.guild.voice_client
                if vc is not None and vc.is_connected():

                    try:
                        await tts.speak(message.guild, vc.channel, response)
                    except Exception as e:
                        print("TTS voice error:", e)
                        await message.channel.send(response)

    await Bot.process_commands(message)



logging.basicConfig(
    handlers=[handler],
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')

Bot.run(token)




