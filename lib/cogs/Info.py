from typing import Optional

from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Member, Embed
from datetime import datetime

class Info(Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('Info')
        print('Info Cog loaded')
        await self.bot.stdout.send('Info cog loaded!')
    
    @command(name="userinfo", aliases=["ui", "UI", "UserInfo", "Userinfo", "userInfo", "MemberInfo", "mi", "MI"])
    async def userinfo(self, ctx, member: Optional[Member]):
        '''Displays the information about the specified user.'''
        member = member or ctx.author

        embed = Embed(
            title="UserInformation",
            colour=member.colour,
            timestamp=datetime.utcnow())
        embed.set_thumbnail(url=member.avatar_url)

        fields = [("Name", str(member), True),
                  ("ID", member.id, True),
                  ("Bot?", member.bot, True),
                  ("Top role", member.top_role.mention, True),
                  ("Status", str(member.status).title(), True),
                  ("Activity", f"{str(member.activity.type).split('.')[-1].title() if member.activity else 'N/A'} {member.activity.name if member.activity else ''}", True),
                  ("Created at", member.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Joined at", member.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Boosted", bool(member.premium_since), True)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=embed)
    
    @command(name="serverrinfo", aliases=["ServerInfo", "Serverinfo", "serverInfo", "si", "SI"])
    async def guildinfo(self, ctx):
      '''Shows information about the server'''
      embed = Embed(
          title="UserInformation",
          colour=ctx.guild.owner.colour,
          timestamp=datetime.utcnow())
      embed.set_thumbnail(url=ctx.guild.icon_url)

      statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                  len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                  len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                  len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

      fields = [("ID", ctx.guild.id, True),
                ("Owner", ctx.guild.owner, True),
                ("Region", ctx.guild.region, True),
                ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                ("Members", len(ctx.guild.members), True),
                ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
                ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
                ("Banned members", len(await ctx.guild.bans()), True),
                ("Statuses", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", True),
                ("Text channels", len(ctx.guild.text_channels), True),
                ("Voice channels", len(ctx.guild.voice_channels), True),
                ("Categories", len(ctx.guild.categories), True),
                ("Roles", len(ctx.guild.roles), True),
                ("Invites", len(await ctx.guild.invites()), True),
                ("\u200b", "\u200b", True)]
                  
      for name, value, inline in fields:
          embed.add_field(name=name, value=value, inline=inline)
      await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))