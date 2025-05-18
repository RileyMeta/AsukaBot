from discord.ext import commands
import discord
import aiohttp
import random
import re
import os

TENOR_API_KEY = os.getenv("TENOR_API_KEY")
TENOR_SEARCH_URL = "https://tenor.googleapis.com/v2/search"
TENOR_TRENDING_URL = "https://tenor.googleapis.com/v2/featured"

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

        choice = random.choice(options)
        await ctx.send(f"I choose {choice}")

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

    @commands.command(name="gif", help="Post a random gif from tenor")
    @commands.has_permissions(embed_links=True)
    async def gif(self, ctx, *, prompt: str = None):
        try:
            async with aiohttp.ClientSession() as session:
                if prompt:
                    url = TENOR_SEARCH_URL
                    params = {
                        "q": prompt,
                        "key": TENOR_API_KEY,
                        "limit": 10,
                        "media_filter": "minimal"
                    }
                else:
                    url = TENOR_TRENDING_URL
                    params = {
                        "key": TENOR_API_KEY,
                        "limit": 10,
                        "media_filter": "minimal"
                    }

                async with session.get(url, params=params) as resp:
                    if resp.status != 200:
                        await ctx.send("Failed to fetch gif", ephemeral=True)
                        return

                    data = await resp.json()
                    results = data.get("results", [])

                    if not results:
                        await ctx.send("No GIFs found.", ephemeral=True)
                        return

                    gif_url = random.choice(results)["media_formats"]["gif"]["url"]
                    await ctx.send(gif_url)

        except discord.Forbidden:
            await ctx.send("I do not have permission to send GIFs")
        except aiohttp.ClientError as e:
            await ctx.send(f"A network error occurred: \n{e}")
        except KeyError:
            await ctx.send("Unexpected API response format.")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: \n{e}")


def setup(bot):
    bot.add_cog(Fun(bot))
