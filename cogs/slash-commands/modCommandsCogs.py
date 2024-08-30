import discord
from discord.ext import commands
from discord import app_commands
from datetime import *
from json import *
from os import *

'''sample of user_info.json format

username:
user_id:
numOfWarns: <how many warnings given>
numOfKicks: <how many kicks given>
numOfmutes: <how many mutes given>
numOfBans: <banned how many times>
datesOfBans: [<when was banned>] (if numOfBans != 0)
unbanned? : (if numOfBans != 0, true or false? If numOfBans == 0, it's null by default)
'''

'''sample of banned_users.json format

guild_id: <id of the guild>
    user_id: reason of last ban,
    user_id: reason of last ban
guild_id2:
    user_id: reason of last ban,
    user_id: reason of last ban
'''

class modCommandsCogs(commands.Cog):
    '''Contains moderation commands for the bot (can be run by moderators only)'''
    def __init__(self, client: commands.Bot):
        self.client = client

        # Paths to different moderation-related JSON files
        base_path = path.dirname(__file__)
        self.user_info_path = path.join(base_path, '../../data/user_info.json')
        self.banned_users_path = path.join(base_path, '../../data/banned_users.json')
        self.warned_users_path = path.join(base_path, '../../data/warned_users.json')

        # Ensure each JSON file exists, create them if they don't
        self.ensure_file_exists(self.user_info_path)
        self.ensure_file_exists(self.banned_users_path)
        self.ensure_file_exists(self.warned_users_path)

    def ensure_file_exists(self, file_path):
        """Ensure the file exists, create it if it doesn't."""
        if not path.exists(file_path):
            with open(file_path, 'w') as f:
                dump({}, f, indent=4)

    def load_data(self, file_path):
        """Load data from a given JSON file."""
        with open(file_path, 'r') as f:
            return load(f)
        
    def save_data(self, file_path, data):
        """Save data to a given JSON file."""
        with open(file_path, 'w') as f:
            dump(data, f, indent=4)

    @app_commands.command(name="ban", description="Ban a user")
    @app_commands.describe(user="The user to ban", reason="Reason for the ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        '''Ban a user'''
        #loading the user_info file
        user_info = self.load_user_info()

        #getting guild id, user id and username for searching in the database
        guild_id = interaction.guild.id
        user_id = user.id
        user_name = user.name

        #getting current date and time
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")

        #checking if user is in the database
        if user_id in user_info[guild_id]:
            numOfBans = user_info[guild_id][user_id]['numOfBans']

            #updating the database
            user_info[guild_id][user_id]['numOfBans'] = numOfBans + 1
            user_info[guild_id][user_id]['datesOfBans'].append(now_str) #adding the date of the ban
            user_info[guild_id][user_id]['unbanned?'] = False

            #saving the database
            self.save_data(user_info)

            #adding the user to the list of currently banned users
            banned_users = self.load_data(self.banned_users_path)

            if guild_id not in banned_users:
                banned_users[guild_id] = {}

            banned_users[guild_id][user_id] = reason
            self.save_data(banned_users)

        #if user is not in the database
        else:
            user_info[guild_id][user_id] = {
                'username' : user_name,
                'user_id' : user_id,
                'numOfWarns' : 0,
                'numOfKicks' : 0,
                'numOfmutes' : 0,
                'numOfBans' : 1,
                'datesOfBans' : [now_str],
                'unbanned?': False
            }

        #sending the embed
        embed = discord.Embed(
            title="Ban",
            description=f"**{user_name}** was banned by **{interaction.user.name}** for **{reason}**.")
    
async def setup(client: commands.Bot) -> None:
    await client.add_cog(modCommandsCogs(client))