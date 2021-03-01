# general bot commands

import discord
from discord.ext import commands


class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # displays developer information
    @commands.command()
    async def creator(self, ctx):
        cinfo = discord.Embed(title="Created by goose", color=0xfffafa)
        cinfo.set_thumbnail(url="https://cdn.discordapp.com/avatars/"
                                "293658485210480640/067f4917d73fafde6855e40e79055067.webp?size=1024")
        cinfo.add_field(name="GitHub", value="github.com/cole-zivkusic")
        cinfo.add_field(name="Discord", value="goose#4609")
        await ctx.send(embed=cinfo)

    # displays available commands
    @commands.command()
    async def info(self, ctx):
        url = self.bot.user.avatar_url
        info = discord.Embed(title="Available commands", color=0xfffafa)
        info.set_thumbnail(url=url)
        info.add_field(name="$rules", value="*A short summary of The Dealer's unique blackjack rules*", inline=False)
        info.add_field(name="$blackjack", value="*Play blackjack with up to 6 of your friends*", inline=False)
        info.add_field(name="$creator", value="*Displays developer information*", inline=False)
        info.set_footer(text="developed by goose#4609 · $creator",
                        icon_url="https://cdn.discordapp.com/avatars/"
                                 "293658485210480640/067f4917d73fafde6855e40e79055067.webp?size=1024")
        await ctx.send(embed=info)

    # displays game rules
    @commands.command()
    async def rules(self, ctx):
        url = self.bot.user.avatar_url
        rules = discord.Embed(title="Game Rules", color=0xfffafa)
        rules.set_thumbnail(url=url)
        rules.add_field(name="Blackjack", value="*- one hand per player, per table*\n"
                                                "*- a simplified version of traditional blackjack*\n"
                                                "*- current support for up to 6 players per table*\n"
                                                "*- there is no betting, thus no splitting, doubling down, etc.*\n"
                                                "**if you have never played blackjack before, google the rules "
                                                "before playing**",
                        inline=False)
        rules.set_footer(text="developed by goose#4609 · $creator",
                         icon_url="https://cdn.discordapp.com/avatars/"
                                  "293658485210480640/067f4917d73fafde6855e40e79055067.webp?size=1024")
        await ctx.send(embed=rules)


def setup(bot):
    bot.add_cog(General(bot))
