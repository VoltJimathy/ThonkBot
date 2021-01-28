from typing import Optional

from discord.ext.commands import Cog, Greedy
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, bot_has_permissions, MissingPermissions, BotMissingPermissions, has_role, MissingRole
from discord import Embed, Member
from datetime import datetime
from ..db import db

class Mod(Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.mod_log = self.bot.get_channel(777500673419902994)
            self.bot.cogs_ready.ready_up('mod')
        print('Mod Cog loaded')
        await self.bot.stdout.send('Mod Cog loaded!')

    @command(name="kick")
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def kick_command(self, ctx, member: Member, *, reason: Optional[str] = "No reason provided."):
        '''Kicks a specified user with the reason provided.
        If no reason is provided, it will be defaulted to "No reason provided."'''
 
        if(ctx.guild.me.top_role.position > member.top_role.position and not member.guild_permissions.administrator):
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
        '''Deletes the specified number of messages.
        If no limit is set, it will delete 5 messages'''
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
        '''Kicks a specified user with the reason provided.
        If no reason is provided, it will be defaulted to "No reason provided."'''
 
        if(ctx.guild.me.top_role.position > member.top_role.position and not member.guild_permissions.administrator):
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

###################################################################################
##   You may want to make a new cog for this, because of how big it already is   ##
##               Just the warn stuff on its own takes up 107 lines               ##
###################################################################################
            
    @command(name="warn", aliases=["w", "wm"])
    @has_role("🚔》Staff")
    async def warn_member(self, ctx, member: Member, *, reason: Optional[str] = "No reason provided"):
        if member != ctx.author:
            if not member.bot:
                if (ctx.author.top_role.position > member.top_role.position and not member.guild_permissions.administrator):
                    db.execute("UPDATE Mod SET Warns = Warns + 1 WHERE UserId = ?",
                               member.id)
                    warns = db.field("SELECT Warns FROM Mod WHERE UserId = ?",
                                      member.id)
                    embed = Embed(
                        title=f"You have been warned",
                        description=f"{ctx.author.display_name} warned you.",
                        colour=0xFF0000,
                        timestamp=datetime.utcnow())
                    embed.set_thumbnail(url=member.avatar_url)

                    fields = [("Reason:", reason, False),
                              ("Number of warns:", str(warns), False)]

                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)

                    await member.send(embed=embed)

                    embed = Embed(
                        title=f"Successfully warned",
                        description=f"{ctx.author.display_name} warned {member.mention}",
                        colour=0xFF0000,
                        timestamp=datetime.utcnow())
                    embed.set_thumbnail(url=member.avatar_url)

                    fields = [("Reason:", reason, False),
                              ("Number of warns:", str(warns), False)]

                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)

                    await ctx.send(embed=embed)

                    embed = Embed(
                        title=f"Successfully warned",
                        description=f"{ctx.author.display_name} warned {member.mention}",
                        colour=0xFF0000,
                        timestamp=datetime.utcnow())
                    embed.set_thumbnail(url=member.avatar_url)

                    fields = [("Reason:", reason, False),
                              ("Number of warns:", str(warns), False)]

                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)

                    await self.mod_log.send(embed=embed)
                else:
                    await ctx.send("That user either has administrator permissions or is higher than you.")
            else:
                await ctx.send("That is a bot. I can't warn bots")
        else:
            await ctx.send("You can't warn yourself")

    @warn_member.error
    async def warn_member_error(self, ctx, error):
        if isinstance(error, MissingRole):
            embed = Embed(title="Missing permissions to use that command",
                          description="You need to be staff to be able to use that command",
                          colour=0xFF0000,
                          timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
        else:
            raise error

    @command(name="warns", aliases=["vw", "warnview"])
    async def check_warns(self, ctx, member: Optional[Member]):
        member = member or ctx.author
        warns = db.field("SELECT Warns FROM Mod WHERE UserId = ?", member.id)

        embed = Embed(title=f"{member.display_name}'s warns",
                      description=f"{member.mention} has {warns} warn(s)",
                      colour=0xFF0000,
                      timestamp=datetime.utcnow())
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

    @command(name="clearwarns", aliases=["clear_warns", "cwarns","cw", "removewarns", "rw"])
    @has_role("🚔》Staff")
    async def remove_member_warns(self, ctx, member: Member, amount: Optional[int]):
        warns = db.field("SELECT Warns FROM Mod WHERE UserId = ?", member.id)
        amount = amount or warns

        db.execute("UPDATE Mod SET Warns = Warns - ? WHERE UserId = ?",
                   amount, member.id)
        new_warns = warns - amount

        embed = Embed(title="Warns removed",
                      colour=0x00FF00,
                      timestamp=datetime.utcnow())
        embed.set_thumbnail(url=member.avatar_url)

        fields = [("Warns removed", str(amount), False),
                  ("Old warns", str(warns), False),
                  ("New warns", str(new_warns), False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Mod(bot))
