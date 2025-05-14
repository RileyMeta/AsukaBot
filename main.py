import os
import time
import discord
from dotenv import load_dotenv
from discord.ext import commands
from const import Colors

CHANNEL_ID = 1266186395127644300
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Load Cogs
def load_cogs():
    cogs_list = ['moderation', 'fun']
    for cog in cogs_list:
        try:
            bot.load_extension(f"cogs.{cog}")
            print(f"{Colors.green}Succesfully loaded cog:{Colors.reset} {cog}")
        except Exception as e:
            print(f"{Colors.red}Failed to load cog:{Colors.reset} {cog}")
            print(f"{Colors.red}{e}{Colors.reset}")

def get_timestamp():
    return time.strftime('%H:%M:%S')

@bot.event
async def on_ready():
    await bot.sync_commands()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over the server"))
    print(f"[{Colors.red}{get_timestamp()}{Colors.reset}] Commands synced.")
    print(f"[{Colors.red}{bot.user}{Colors.reset} @ {Colors.red}{get_timestamp()}{Colors.reset}] EVA Unit 2, Standing By.")

@bot.event
async def stop():
    print(f"[Time: {get_timestamp()}]")
    print(f"[{Colors.yellow}ALERT{reset}] EVA Unit 2, Offline.")

if __name__ == "__main__":
    load_cogs()
#    bot.load_extension("cogs.moderation")
    intents.message_content = True
    intents.members = True
    bot.run(TOKEN)
