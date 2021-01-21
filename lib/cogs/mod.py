from typing import Optional

from discord.ext.commands import Cog, Greedy
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, bot_has_permissions, MissingPermissions, BotMissingPermissions
from discord import Embed, Member
from datetime import datetime

class Mod(Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('mod')
        print('Mod Cog loaded')
        await self.bot.stdout.send('Mod Cog loaded!')

    @command(name="kick")
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def kick_command(self, ctx, member: Member, *, reason: Optional[str] = "No reason provided."):
 
                if(ctx.guild.me.top_role.position > member.top_role.position
                and not member.guild_permissions.administrator):
                    await member.kick(reason=reason)

                    embed = Embed(
                        title="Member Kicked",
                        colour=0xDD2222,
                        timestamp=datetime.utcnow())
                    embed.set_thumbnail(url=member.avatar_url)
                    fields = [("Member", f"{member.display_name}", False),
                              ("Actioned by:", ctx.author.display_name, False),
                              ("Reason:", reason, False)]
                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)
                    await ctx.send(embed=embed)

    @kick_command.error
    async def kick_command_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = Embed(
                title="Missing Permissions",
                description="You are missing the correct permissions to run this command",
                colour=0xDD2222,
                timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
        elif isinstance(error, BotMissingPermissions):
            embed = Embed(
                title="Missing Permissions",
                description="I do not have the correct permissions to run this command",
                colour=0xDD2222,
                timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
    
    @command(name="clear", aliases=["purge"])
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, limit: Optional[int] = 5):
        with ctx.channel.typing():
            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=limit)
            embed = Embed(
                title="Cleared Messages",
                description=f"I have cleared {len(deleted)} messages",
                colour=0xFF0000,
                timestamp=datetime.utcnow())
            await ctx.send(embed=embed, delete_after=5)
    
    @clear_messages.error
    async def clear_messages_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = Embed(
                title="Missing Permissions",
                description="You are missing the correct permissions to run this command",
                colour=0xFF0000,
                timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
        elif isinstance(error, BotMissingPermissions):
            embed = Embed(
                title="Missing Permissions",
                description="I do not have the correct permissions to run this command",
                colour=0xFF0000,
                timestamp=datetime.utcnow())
            await ctx.send(embed=embed)

    @command(name="ban")
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def ban_command(self, ctx, member: Member, *, reason: Optional[str] = "No reason provided."):
 
                if(ctx.guild.me.top_role.position > member.top_role.position
                and not member.guild_permissions.administrator):
                    await member.ban(reason=reason)

                    embed = Embed(
                        title="Member Banned",
                        colour=0xDD2222,
                        timestamp=datetime.utcnow())
                    embed.set_thumbnail(url=member.avatar_url)
                    fields = [("Member", f"{member.display_name}", False),
                              ("Actioned by:", ctx.author.display_name, False),
                              ("Reason:", reason, False)]
                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)
                    await ctx.send(embed=embed)

    @ban_command.error
    async def ban_command_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = Embed(
                title="Missing Permissions",
                description="You are missing the correct permissions to run this command",
                colour=0xDD2222,
                timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
        elif isinstance(error, BotMissingPermissions):
            embed = Embed(
                title="Missing Permissions",
                description="I do not have the correct permissions to run this command",
                colour=0xDD2222,
                timestamp=datetime.utcnow())
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Mod(bot))