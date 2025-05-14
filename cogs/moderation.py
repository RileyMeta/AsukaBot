import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command()
    async def serverinfo():
        pass

    @commands.command()
    async def userinfo(user):
        pass

    @commands.command()
    async def avatar(user):
        pass

    @discord.slash_command(name="kick", description="Kick a user from the server.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason: str = "No reason provided."):
        if member == ctx.author:
            await ctx.respond("You can't kick yourself, idiot!", ephemeral=True)
            return
        else:
            try:
                await member.kick(reason=reason)
                await ctx.respond(f"{member.mention} has been kicked. \nReason: {reason}")
            except discord.Forbidden:
                await ctx.respond(f"I'm sorry, I do not have permission to kick that member.")
            except Exception as e:
                await ctx.respond(f"An error occurred: {e}", ephemeral=True)

# Saving for later
#    async def ban(self, ctx, member: discord.Member, reason: str = "No reason provided."):

    @discord.slash_command(name="ban", description="Ban a user from the server.")
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Member,
        reason: str = "No reason provided."
    ):
        if not ctx.guild:
            await ctx.respond("This command must be used in a server.", ephemeral=True)
            return

        if member == ctx.author:
            await ctx.respond(f"You can't ban yourself.", ephemeral=True)
            return

        if member == self.bot.user:
            await ctx.respond("I can't ban myself, idiot.")
            return

        try:
            await member.ban(reason=reason)
            await ctx.respond(f"{member.mention} has been banned. \nReason: {reason}")
        except discord.Forbidden:
            await ctx.respond(f"I'm sorry, I do not have permission to ban that member.", ephemeral=True)
        except Exception as e:
            await ctx.respond(f"An error occurred: {e}", ephemeral=True)

    async def unban(user):
        pass

    async def mute(user):
        pass

    async def clear():
        pass

    # Error handling
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You don't have permission to kick memebers.", ephemeral=True)
        else:
            await ctx.respond("An error occurred: {error}", ephemeral=True)

    @ban.error
    async def ban_error(self, ctx: discord.ApplicationContext, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You don't have permission to ban members.", ephemeral=True)
        else:
            await ctx.respond(f"Unexpected Error: {error}", ephemeral=True)

def setup(bot):
    bot.add_cog(Moderation(bot))
