import time
import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", help="Ping the bot to see it's latency.")
    async def ping(self, ctx):
        start_time = time.perf_counter()
        message = await ctx.send("Pong!")
        end_time = time.perf_counter()

        latency = self.bot.latency * 1000 # in ms
        overall = (end_time - start_time) * 1000

        await message.edit(content=f"Pong!\nLatency: {latency:.2f}ms")
        # await message.edit(content=f"\n{overall:.2f}ms")

    @commands.command(name="serverinfo", help="Show information about the server.")
    @commands.cooldown(rate=1, per=60.0, type=commands.BucketType.user)
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

    @commands.command(name="userinfo", help="Show information about a user")
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.user)
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        user = member._user if hasattr(member, "_user") else member

        embed = discord.Embed(
            title=f"User Info: {member.display_name}",
            color=discord.Color.teal(),
            timestamp=ctx.message.created_at
        )

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="User ID", value=member.id, inline=False)
        embed.add_field(name="Username", value=f"{member.name}#{member.discriminator}", inline=False)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)

        try:
            fetched_user = await ctx.bot.fetch_user(member.id)
            if hasattr(fetched_user, "pronouns") and fetched_user.pronouns:
                embed.add_field(name="Pronouns", value=fetched_user.pronouns, inline=False)
        except Exception as e:
            pass

        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

    @commands.command(name="avatar", help="Display the profile picture of a user")
    @commands.cooldown(rate=1, per=60.0, type=commands.BucketType.user)
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author # Default to you if you don't provide a member

        embed = discord.Embed(
            title=f"{member.display_name}",
            color=discord.Color.og_blurple()
        )
        embed.set_image(url=member.display_avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

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

    @discord.slash_command(name="mute", description="Mute a user on the server.")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason="No reason provided"):
        guild = ctx.guild
        muted_role = discord.utils.get(guild.roles, name="muted")

        if not muted_role:
            try:
                muted_role = await guild.create_role(name="muted", reason="Needed for muting members.")
                for channel in guild.Channels:
                    await channel.set_permissions(muted_role, send_messages=False, speak=False)
            except discord.Forbidden:
                return await ctx.send("I don't have permission to create the muted role.")

        if muted_role in member.roles:
            await ctx.send(f"{member.mention} is already muted.")
            return

        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f"{member.mention} has been muted.\nReason: {reason}")

    @discord.slash_command(name="unmute", description="Unmute a user that was previously muted")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason="No reason provided"):
        guild = ctx.guild
        muted_role = discord.utils.get(guild.roles, name="muted")

        if not muted_role:
            await ctx.send("There is not `muted` role in this server.")
            return

        if muted_role not in member.roles:
            await ctx.send(f"{member.mention} is not muted.")
            return

        try:
            await member.remove_roles(muted_role, reason="Unmuted by command")
            await ctx.send(f"{member.mention} has been unmuted.")
        except discord.Forbidden:
            await ctx.send("I do not have permission to remove that role", ephemeral=True)
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command(name="clear", help="Delete a number of messages from the chat. (e.g, !clear 10)")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 0):
        if amount < 1:
            await ctx.send("Please specify a number of messages.", ephemeral=True)
            return

        try:
            # +1 to include user's command `msg = !clear 10` = 10 + msg
            deleted = await ctx.channel.purge(limit=amount + 1)
        except discord.Forbidden:
            await ctx.send("I don't have permission to delete messages.")
        except Exception as e:
            await ctx.send(f"Unexpected error: {e}")

    @commands.has_permissions(send_polls=True)
    async def poll(question, options = []):
        pass


    ############################
    #      Error handling      #
    ############################
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You don't have permission to kick memebers.")
        else:
            await ctx.respond("An error occurred: {error}")

    @ban.error
    async def ban_error(self, ctx: discord.ApplicationContext, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You don't have permission to ban members.")
        else:
            await ctx.respond(f"Unexpected Error: {error}")

    @unban.error
    async def unban_error(self, ctx: discord.ApplicationContext, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You don't have permission to use this command.")
        else:
            await ctx.respond(f"Unexpected error: {error}")

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please enter a valid number.")
        else:
            await ctx.send(f"An error occurred: {e}")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to mute users")
        elif isinstance(error, commands.MissinRequiredArgument):
            await ctx.send("Usage: `/mute @user [reason]`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please mention a valid user.")
        else:
            await ctx.send(f"An error occurred: {error}")

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        elif isinstance(error, commands.MissinRequiredArgument):
            await ctx.send("Usage: `/unmute @user`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please mention a valid user.")
        else:
            await ctx.send(f"An error occurred: {error}")

def setup(bot):
    bot.add_cog(Moderation(bot))
