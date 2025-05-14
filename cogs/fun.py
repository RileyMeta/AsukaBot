import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hello", help="Say hello to the bot")
    async def hello(self, ctx):
        greetings = ['Hi', 'Hello', 'Hi there']
        greeting = random.randrange(len(greetings))
        await ctx.send(greetings[greeting])

    @commands.command(name="roll", help="roll a dice with any number of sides (e.g, !roll 20)")
    async def roll(self, ctx, sides: int):
        if sides < 1:
            await ctx.send("Cannot roll a die with less than 2 sides. Use !flip for 50/50")
            return

        num = random.randrange(0, sides)

        await ctx.send(num)

    @commands.command(name="flip", help="Flip a coin: heads or tails")
    async def flip(self, ctx):
        num = random.randrange(0, 2)
        if num == 0:
            prompt = "Heads"
        else:
            prompt = "Tails"
        await ctx.send(prompt)

    @discord.slash_command(name="gm", description="Have the bot say good morning")
    async def gm(self, ctx):
        a = ['Good Morning!', 'Morning']
        x = random.randrange(len(a))
        await ctx.respond(a[x])

    @discord.slash_command(name="bye", description="Have the bot say goodbye to you")
    async def bye(self, ctx):
        a = ["bye bye", "goodbye", "later", "cya"]
        x = random.randrange(len(a))
        await ctx.respond(a[x])

    @commands.command(name="say", help="Have Asuka say something")
    @commands.has_permissions(send_messages=True)
    async def say(self, ctx, *, message: str = "Idiot forgot to make me say something"):
        await ctx.message.delete()
        await ctx.send(message)

def setup(bot):
    bot.add_cog(Fun(bot))
