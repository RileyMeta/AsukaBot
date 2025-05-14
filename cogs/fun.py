import discord
from discord.ext import commands
import random
import re

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

    @commands.command(name="choose", help="Have the bot randomly choose from a list of options")
    @commands.has_permissions(send_messages=True)
    async def choose(self, ctx, *options):
        if len(options) < 2:
            await ctx.send("Baka, provide at least 2 options!")
            return

        choice = random.randrange(len(options) - 1)
        await ctx.send(f"I choose {options[choice]}")

    @commands.command(name="mock", help="hAvE ThE bOt MoCk A MeSsAgE")
    @commands.has_permissions(send_messages=True)
    async def mock(self, ctx, *, text):
        mocked = ""
        upper = False
        for char in text:
            if char.isalpha():
                mocked += char.upper() if upper else char.lower()
                upper = not upper
            else:
                mocked += char

        await ctx.send(mocked)

    @commands.command(name="uwu", help="UwU-ify any message")
    @commands.has_permissions(send_messages=True)
    async def uwu(self, ctx, *, text):
        faces = ["(・`ω´・)", "uwu", ">w<", "^w^", "(*^ω^)", "(⑅˘꒳˘)", "(✿◠‿◠)"]

        uwu_text = text
        uwu_text = re.sub(r'[rl]', 'W', uwu_text)
        uwu_text = re.sub(r'[RL]', 'W', uwu_text)
        uwu_text = re.sub(r'n([aeiou])', r'ny\1', uwu_text)
        uwu_text = re.sub(r'N([aeiouAEIOU])', r'Ny\1', uwu_text)

        uwu_text += " " + random.choice(faces)

        await ctx.send(uwu_text)

def setup(bot):
    bot.add_cog(Fun(bot))
