from discord.ext import commands
from datetime import datetime
import subprocess
import platform
import discord
import distro
import psutil
import shutil
import os

class Neofetch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_cpu_name(self):
        if platform.system() == "Windows":
            return platform.processor()
        elif platform.system() == "Darwin":
            command = "/usr/sbin/sysctl -n machdep.cpu.brand_string"
            return os.popen(command).read().strip()
        elif platform.system() == "Linux":
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":")[1].strip()
        return "Unknown CPU"

    def get_kernel(self):
        if platform.system() == "Linux":
            return distro.name()
        else:
            return platform.system()

    def get_uptime(self):
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        now = datetime.now()
        uptime = now - boot_time
        return str(uptime).split('.')[0]

    def get_shell(self):
        return os.environ.get('SHELL', 'unknown')

    def get_architecture(self):
        return platform.release()

    def get_terminal(self):
        return os.environ.get('TERM', 'unknown')

    def get_ram(self):
        mem = psutil.virtual_memory()
        used = mem.total - mem.available
        return f"{used // (1024**3)}GiB / {mem.total // (1024**3)}GiB"

    def get_swap(self):
        swap = psutil.swap_memory()
        total_swap = swap.total / 1024 ** 3
        used_swap = swap.used / 1024 ** 3
        return total_swap, used_swap

    def get_disk(self):
        total, used, _ = shutil.disk_usage("/")
        return f"{used // (1024**3)}GiB / {total // (1024**3)}GiB"

    @commands.command(name="neofetch", help="Print information about the server the bot is using.")
    @commands.has_permissions(send_messages=True)
    async def neofetch(self, ctx):
        username = os.getlogin()
        hostname = platform.node()
        total_swap, used_swap = self.get_swap()
        arch = platform.machine()

        embed = discord.Embed(
            title=f"{username}@{hostname}",
            color=discord.Color.blue()
        )

        embed.add_field(name="OS", value=f"{self.get_kernel()} {arch}", inline=False)
        embed.add_field(name="Kernel", value=f"{platform.system()} {self.get_architecture()}", inline=False)
        embed.add_field(name="Uptime", value=f"{self.get_uptime()}", inline=False)
        embed.add_field(name="Shell", value=f"{self.get_terminal()}", inline=False)
        embed.add_field(name="CPU", value=f"{self.get_cpu_name()}", inline=True)
        embed.add_field(name="Memory", value=f"{self.get_ram()}", inline=False)
        embed.add_field(name="Swap", value=f"{used_swap:.2f}GiB / {total_swap:.2f}GiB", inline=False)
        embed.add_field(name="Disk", value=f"{self.get_disk()}", inline=False)

        embed.timestamp = discord.utils.utcnow()

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Neofetch(bot))
