import discord
from discord import app_commands
from discord.ext import commands, tasks
import time
import os
import dotenv
import typing
from asyncio import *
import random

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('v!'), intents=discord.Intents().all())

        self.cogsList = []
        self.status_messages = [
            {"type": discord.ActivityType.playing, "message": "epic tales and managing server drama"},
            {"type": discord.ActivityType.playing, "message": "and breaking things, one command at a time"},
            {"type": discord.ActivityType.playing, "message": "the role of a professional procrastinator"},
            {"type": discord.ActivityType.playing, "message": ": \"working hard or hardly working?\" Nah, definitely the latter"},

            {"type": discord.ActivityType.streaming, "message": "my life as your server's unpaid intern"},
            {"type": discord.ActivityType.streaming, "message": "the art of avoiding responsibilities"},
            {"type": discord.ActivityType.streaming, "message": "how to pretend to be competent"},
            {"type": discord.ActivityType.streaming, "message": "the chronicles of your server drama"},

            {"type": discord.ActivityType.watching, "message": "but too cool for actual work"},
            {"type": discord.ActivityType.watching, "message": "your problems from afar"},
            {"type": discord.ActivityType.watching, "message": "the server while owner holds up her shits"},
            {"type": discord.ActivityType.watching, "message": "my questionable life choices"}
]

        self.status_types = [
            discord.Status.online,
            discord.Status.dnd,
            discord.Status.idle
        ]
        self.current_status_index = 0
        self.current_type_index = 0
        

    async def setup_hook(self):
        if self.cogsList:
            for ext in self.cogsList:
                await self.load_extension(ext)


    @tasks.loop(minutes=5)
    async def change_status(self):
        status = random.choice(self.status_messages)
        activity = discord.Activity(type=status["type"], name=status["message"])
        status_type = random.choice(self.status_types)
        await self.change_presence(status=status_type, activity=activity)

    
    async def on_ready(self):
        print(f"Logged in as {self.user.name}")
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} commands.")
        except Exception as e:
            print(e)
        if not self.change_status.is_running():
            self.change_status.start()
        print("------------------------------------------------")

dotenv.load_dotenv()

client = Client()
client.run(os.getenv("BOT_TOKEN"))
