import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", help="Ping the bot to see if it's online.")
    async def ping(self, ctx):
        await ctx.send("Pong!")


    @commands.command(name="serverinfo", help="Show information about the server.")
    async def serverinfo(self, ctx):
        guild = ctx.guild

        embed = discord.Embed(
            title=guild.name,
            color=discord.Color.blurple()
        )

        embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)

        embed.add_field(name="Owner", value=f"{guild.owner}", inline=False)
        embed.add_field(name="Members", value=f"{guild.member_count}", inline=True)
        embed.add_field(name="roles", value=len(guild.roles), inline=True)

        role_name = "moderators"
        role = discord.utils.get(guild.roles, name=role_name)

        if role:
            mods = [member.name for member in guild.members if role in member.roles]

            if not mods:
                value = "None"
            else:
                value = ", ".join(mods[:10]) # Show only 10 for readability
                if len(mods) > 10:
                    value += f" ...and {len(mods) - 10} more"

            embed.add_field(name=f"{role.name}", value=value, inline=False)
        else:
            embed.add_field(name="Admins", value="Role not found", inline=False)

        text_channels = len([c for c in guild.text_channels])
        voice_channels = len([c for c in guild.voice_channels])
        embed.add_field(name="Text Channels", value=text_channels, inline=False)
        embed.add_field(name="Voice Channels", value=voice_channels, inline=False)

        embed.add_field(name="Created On", value=guild.created_at.strftime("%b %d, %Y"), inline=False)

        await ctx.send(embed=embed)

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

    @discord.slash_command(name="unban", description="Unban a previously banned user.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: str, reason: str = "No reason provided."):
        if not ctx.guild:
            await ctx.respond("This command must be used in a server.", ephemeral=True)
            return

        banned_users = [entry async for entry in ctx.guild.bans()]

        target_user = None
        for ban_entry in banned_users:
            banned_user = ban_entry.user
            # Match either name#tag or id
            if (
                f"{banned_user.name}#{banned_user.discriminator}" == user
                or str(banned_user.id) == user
                ):
                    target_user = banned_user
                    break

        if target_user is None:
            await ctx.respond("User was not found in ban list.", ephemeral=True)
            return

        try:
            await ctx.guild.unban(target_user, reason=reason)
            await ctx.respond(f"{target_user.name}#{target_user.discriminator} has been unbanned\nReason: {reason}")
        except discord.Forbidden:
            await ctx.respond("I don't have permission to unban that user.", ephemeral=True)
        except Exception as e:
            await ctx.respond(f"An error occurred: {e}", ephemeral=True)

    @commands.command(name="mute", help="Mute a user on the server.")
    async def mute(user):
        pass

    @commands.command(name="clear", help="Delete a number of messages from the chat. (e.g, !clear 10)")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 0):
        if amount < 1:
            await ctx.send("Please specify a number of messages.")
            return

        try:
            # +1 to include user's command `msg = !clear 10` = 10 + msg
            deleted = await ctx.channel.purge(limit=amount + 1)
        except discord.Forbidden:
            await ctx.send("I don't have permission to delete messages.")
        except Exception as e:
            await ctx.send(f"Unexpected error: {e}")


    ############################
    #      Error handling      #
    ############################
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

    @unban.error
    async def unban_error(self, ctx: discord.ApplicationContext, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You don't have permission to use this command.", ephemeral=True)
        else:
            await ctx.respond(f"Unexpected error: {error}", ephemeral=True)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please enter a valid number.")
        else:
            await ctx.send(f"An error occurred: {e}")



def setup(bot):
    bot.add_cog(Moderation(bot))
