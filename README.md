T.E.M.P.E.S.T

A Modular Framework for Discord AI Chatbots Powered by Ollama

Overview

T.E.M.P.E.S.T is a Python-based framework designed for building advanced AI-driven Discord chatbots using Ollama as the local LLM backend.
It provides a modular architecture supporting:

Conversational AI with persistent memory

Vision-based message understanding (image input)

Text-to-Speech (TTS) voice interaction in Discord voice channels

Command-based extensibility via Discord cogs

Config-driven behavior for easy customization

The framework is intended for developers who want fine-grained control over AI behavior while keeping inference fully local.

Features

Local LLM inference via Ollama

Multi-modal support

Text chat

Image understanding (vision models)

Voice output via TTS

Persistent conversation memory

Discord command framework

Owner-restricted administrative commands

Configurable permissions and channels

Voice channel auto-response

Graceful shutdown and memory reset utilities

Architecture
.
├── main.py              # Bot entry point and event handling
├── main_commands.py     # Core Discord commands (Cog)
├── vision.py            # Image + vision model handling
├── tts.py               # Text-to-Speech and voice playback
├── memory.py            # Persistent conversation memory
├── config.json          # Runtime configuration
├── system.txt           # System prompt for the AI
├── memory.json          # Runtime memory store (generated)
├── requirements.txt     # Python dependencies

Requirements
System Requirements

Python 3.10+

Discord Bot Token

Ollama installed and running locally

FFmpeg available in system PATH (for voice playback)

CUDA-compatible GPU (optional, for TTS acceleration)

Python Dependencies

Install dependencies using:

pip install -r requirements.txt


requirements.txt includes:

discord.py

ollama

torch

TTS

aiohttp

Pillow

Configuration

All runtime configuration is handled through config.json.

Example config.json
{
  "discord_token": "YOUR_DISCORD_BOT_TOKEN",
  "chat_model": "qwen3",
  "voice_model": "llama3.2",
  "permitted_channels": [
    123456789012345678
  ],
  "welcome": {
    "SERVER_ID": "CHANNEL_ID"
  },
  "startup_channel": 123456789012345678,
  "memory_max_size": 25,
  "gifs": [
    "https://example.gif"
  ],
  "owner": "your_discord_username",
  "temp": 0.7,
  "num_gpu": 1
}


Note: Channel and server IDs must be integers, not strings, when used by Discord.py.

System Prompt

The file system.txt contains the system prompt used to define the personality and behavior of the AI.
This prompt is injected into the conversation context and should be customized per bot instance.

Running the Bot

Ensure Ollama is running:

ollama serve


Start the bot:

python main.py


On startup, the bot will:

Change its username

Send a startup message in the configured channel

Begin listening for mentions in permitted channels

Usage
Chat Interaction

The bot only responds when mentioned

Responses are restricted to configured channels

Conversation history is persisted in memory.json

Vision

If a message contains an image attachment or embed, the vision pipeline is automatically invoked

Images are resized, encoded, and passed to a vision-capable Ollama model

Voice

If the bot is connected to a voice channel, responses are spoken using TTS

Otherwise, text responses are sent normally

Commands

Command prefix: //

General Commands

//join – Join the user’s voice channel

//leave – Leave the current voice channel

//annoy <n> – Send random GIFs (limited to permitted channels)

Owner-Only Commands

//forget – Wipe conversation memory

//dm <user> <message> – Send a direct message as the bot

//auto_shutdown <seconds> – Gracefully shut down the bot and host machine
