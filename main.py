import os
import time
import discord
from dotenv import load_dotenv
from discord.ext import commands
from const import Colors
import random

load_dotenv()
WELCOMES = int(os.getenv("WELCOMES"))
LEAVES = int(os.getenv("LEAVES"))
LOGS = int(os.getenv("LOGS"))
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Dynamically Load Cogs from the `./cogs/` folder
def load_cogs():
    cogs_list = ['moderation', 'fun', 'automod', 'reminder']
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
    print(f"\n[{Colors.yellow}ALERT{Colors.reset} @ {Colors.yellow}{get_timestamp()}{Colors.reset}] EVA Unit 2, Offline.")

@bot.event
async def on_member_join(member):
    messages = [
            f"Welcome, {member.mention}. Report to the command center — Ikari doesn't like slackers.",
            f"Congratulations {member.mention}! You've been selected for synchronization.",
            f"Welcome to the GeoFront {member.mention}. Try not to cause a Third Impact.",
            f"{member.mention}\nAnother soul joins Nerv. Try not to annoy me as much as Shinji does.",
            f"Initiating entry plug sequence... Welcome aboard, {member.mention}.",
            f"Welcome {member.mention}! We were starting to think you were another dummy plug.",
            f"{member.mention}\nSync ratio rising — we’ve got a new member!",
            f"{member.mention}\nWelcome to NERV HQ. Don't worry, we won't make you pilot an Eva... probably."
    ]

    choice = random.choice(messages)

    channel = member.guild.get_channel(WELCOMES)

    if channel:
        await channel.send(choice)
    else:
        printf(f"Warning: Could not find channel with ID {WELCOMES}")

@bot.event
async def on_member_remove(member):
    messages = [
            f"{member.display_name}\nAnother soul departs from the command center. Sync ratio lost.",
            f"{member.display_name}\nConnection terminated. Their mission here is complete.",
            f"{member.display_name} has ejected. The LCL will settle without them.",
            f"{member.display_name}\nOne less plug in the system. Hold the line.",
            f"{member.display_name} left the GeoFront. Let’s hope the Angels don’t notice.",
            f"{member.display_name} has gone radio silent. God’s in his heaven, all’s right with the world…?",
            f"{member.display_name}\nAnd just like that, another presence fades from the AT Field.",
            f"{member.display_name} vanished into the void. Stay strong, pilots.",
            f"{member.display_name} logged out of the simulation. Reality awaits.",
            f"{member.display_name}\nAnother entry plug disengaged. Safe travels, pilot."
    ]

    choice = random.choice(messages)

    channel = member.guild.get_channel(LEAVES)

    if channel:
        await channel.send(choice)
    else:
        printf(f"Warning: Could not find channel with ID {LEAVES}")

@bot.event
async def on_message_edit(before, after):
    # Ignore DMs
    if not before.guild:
        return

    # Ignore bot messages
    if before.author.bot:
        return

    # Ignore unchanged content
    if before.content == after.content:
        return

    report_channel = bot.get_channel(LOGS)
    if report_channel:
        embed = discord.Embed(
            color=discord.Color.orange(),
            description=f"[**Message**]({after.jump_url}) edited in **{before.channel.mention}**"
        )
        embed.set_author(
            name=str(before.author),
            icon_url=before.author.display_avatar.url
        )
        embed.add_field(name="Before", value=before.content or "*No content*", inline=False)
        embed.add_field(name="After", value=after.content or "*No content*", inline=False)
        embed.timestamp = after.edited_at

        await report_channel.send(embed=embed)

@bot.event
async def on_message_delete(message):
    # Same as function above, ignore DMs and Bots
    if not message.guild:
        return

    if message.author.bot:
        return

    report_channel = bot.get_channel(LOGS)
    if report_channel:
        embed = discord.Embed(
            color=discord.Color.red(),
            description= f"[**Message**]({message.jump_url}) deleted in {message.channel.mention}"
        )
        embed.set_author(
            name=str(message.author),
            icon_url=message.author.display_avatar.url
        )
        embed.add_field(name="Deleted Message", value=message.content or "*No content*", inline=False)
        embed.timestamp = discord.utils.utcnow()

        await report_channel.send(embed=embed)

if __name__ == "__main__":
    load_cogs()
    intents.message_content = True
    intents.members = True
    bot.run(TOKEN)
    stop()
