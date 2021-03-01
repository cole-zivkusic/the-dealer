# The Dealer
# last updated 02/26/21

import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="$", intents=intents)
extensions = ["general", "blackjack"]

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)

# replaced with $info
bot.remove_command("help")


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord.')
    for guild in bot.guilds:
        print(guild.name + " (id: " + str(guild.id) + ")")

    game = discord.Game("The Dealer · $info")
    await bot.change_presence(status=discord.Status.online, activity=game)

bot.run(TOKEN)
