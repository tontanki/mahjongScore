import discord
from discord.ext import commands
from player.playerData import PlayerData

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

players = PlayerData()


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
