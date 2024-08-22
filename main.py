import discord
from discord import app_commands
from discord.ext import commands, tasks
import time
import os
import dotenv
import typing
from asyncio import *


class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('v!'), intents=discord.Intents().all())

        self.cogsList = []
        self.status_messages = [
            "Making friends with your server members",
            "Writing epic tales and managing server drama",
            "Too cool for actual work",
            "Breaking things, one command at a time",
            "Running on caffeine and questionable life choices",
            "Too busy to care about your problems",
            "Professional procastinator at your service",
            "Holding up the server for you",
            "Avoiding responsibilities like a champ",
            "Just another day of pretending to be competent",
            "Your server's unpaid intern",
            "Working hard or hardly working? Definitely the latter"
        ]
        self.status_types = [
            discord.Status.online,
            discord.Status.dnd,
            discord.Status.idle
        ]
        self.current_status_index = 0
        self.current_type_index = 0

        self.change_status.start()
        

    async def setup_hook(self):
        if self.cogsList:
            for ext in self.cogsList:
                await self.load_extension(ext)


    @tasks.loop(minutes=5)
    async def change_status(self):
        status_message = self.status_messages[self.current_status_index]

        status_type = self.status_types[self.current_type_index]

        await self.change_presence(status=status_type, activity=discord.Game(name=status_message))

        self.current_status_index = (self.current_status_index + 1) % len(self.status_messages)

        self.current_type_index = (self.current_type_index + 1) % len(self.status_types)

    
    async def on_ready(self):
        print(f"Logged in as {self.user.name}")
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} commands.")
        except Exception as e:
            print(e)
        print("------------------------------------------------")

dotenv.load_dotenv()

client = Client()
client.run(os.getenv("BOT_TOKEN"))
