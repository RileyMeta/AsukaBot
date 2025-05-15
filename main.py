import os
import time
import discord
from dotenv import load_dotenv
from discord.ext import commands
from const import Colors
import random

load_dotenv()
CHANNEL_ID = os.getenv("BOT_CHANNEL")
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

def stop():
    print(f"\n[{Colors.yellow}ALERT @ {get_timestamp()}{Colors.reset}] EVA Unit 2, Offline.")

@bot.event
async def on_member_join(member):
    messages = [
            "Welcome, new pilot. Report to the command center — Ikari doesn't like slackers.",
            "Congratulations! You've been selected for synchronization.",
            "Welcome to the GeoFront. Try not to cause a Third Impact.",
            "Another soul joins Nerv. Try not to annoy me as much as Shinji does.",
            "Initiating entry plug sequence... Welcome aboard, Rookie.",
            "Welcome! We were starting to think you were another dummy plug.",
            "Sync ratio rising — we’ve got a new member!",
            "Welcome to NERV HQ. Don't worry, we won't make you pilot an Eva... probably."
    ]

    choice = random.randrange(len(messages) - 1)

    channel_id = 1292201687552888872
    channel = member.guild.get_channel(channel_id)

    if channel:
        await channel.send(f"{member.mention}\n{messages[choice]}")

@bot.event
async def on_member_remove(member):
    messages = [
            "Another soul departs from the command center. Sync ratio lost.",
            "Connection terminated. Their mission here is complete.",
            "Pilot has ejected. The LCL will settle without them.",
            "One less plug in the system. Hold the line.",
            "They’ve left the GeoFront. Let’s hope the Angels don’t notice.",
            "They’ve gone radio silent. God’s in his heaven, all’s right with the world…?",
            "And just like that, another presence fades from the AT Field.",
            "One more vanishes into the void. Stay strong, pilots.",
            "They’ve logged out of the simulation. Reality awaits.",
            "Another entry plug disengaged. Safe travels, pilot."
    ]

    choice = random.randrange(len(messages) - 1)

    channel_id = 1292201687552888872
    channel = member.guild.get_channel(channel_id)

    if channel:
        await channel.send(f"{member.display_name}\n{messages[choice]}")

if __name__ == "__main__":
    load_cogs()
    intents.message_content = True
    intents.members = True
    bot.run(TOKEN)
    stop()
