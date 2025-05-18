import re
import asyncio
import discord
from discord.ext import commands

class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def parse_time(self, time_str):
        """ Parse time string by incriments: 10s, 5m, 2h into seconds """
        match = re.fullmatch(r"(\d+)([smh])", time_str.lower())
        if not match:
            return None

        num, unit = match.groups()
        num = int(num)

        if unit == 's':
            return num
        elif unit == 'm':
            return num * 60
        elif unit == 'h':
            return num * 3600
        return None

    @commands.command(name="reminder", help="Set a reminder.\nUsage !reminder <dm: True/False> <time> <message>")
    @commands.has_permissions(send_messages=True)
    async def reminder(self, ctx, dm: bool, time: str, *, prompt: str):
        seconds = self.parse_time(time)
        if seconds is None:
            await ctx.send("Invalid time format! Use `10s`, `5m` or `1h`.")
            return

        await ctx.send(f"Got it! I'll remind you in {time}")
        await asyncio.sleep(seconds)

        if dm:
            try:
                await ctx.author.send(f"Don't forget: {prompt}")
            except discord.Forbidden:
                await ctx.send("Couldn't send you a DM. Do you have DMs disabled?")
        else:
            await ctx.send(f"{ctx.author.mention} Don't Forget! {prompt}")

def setup(bot):
    bot.add_cog(Reminder(bot))
