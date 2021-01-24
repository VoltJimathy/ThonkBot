from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions, CheckFailure
from discord import Embed
from discord import __version__ as discord_version
from datetime import datetime, timedelta
from ..db import db # type: ignore
from psutil import Process, virtual_memory
from platform import python_version
from time import time

class Misc(Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('Misc')
        print('Misc Cog loaded')
        await self.bot.stdout.send('Misc cog loaded!')

    @command(name="set_prefix", aliases=["SetPrefix", "Prefix"])
    @has_permissions(manage_guild=True)
    async def set_prefix(self, ctx, new: str):
        """Changes the prefix of the bot for your server"""
        db.execute("UPDATE Guilds SET Prefix = ? WHERE GuildID = ?", new, ctx.guild.id)
        db.commit()
        await ctx.send(f"I have changed this servers prefix to {new}")

    @set_prefix.error
    async def change_prefix_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            embed = Embed(
                title="You can't change the servers prefix",
                description="You need to Manage Guild permissions to do that command",
                colour=0xFF0000,
                timesptamp=datetime.utcnow())
            await ctx.send(embed=embed)
    
    @command(name="info", aliases=["stats"])
    async def info(self, ctx):
        embed = Embed(
            title="Bot stats",
            colour=ctx.author.colour,
            thumbnail=self.bot.user.avatar_url,
            timestamp=datetime.utcnow())
        
        proc = Process
        with proc.oneshot(self=self):
            uptime = timedelta(seconds=time()-proc.create_time())
            cpu_time = timedelta(seconds=(cpu := proc.cpu_times()).system + cpu.user)
            mem_total = virtual_memory().total / (1024**2)
            mem_of_total = proc.memory_percent()
            mem_usage = mem_total / (mem_of_total*100)
        
        fields = [("Bot version", self.bot.VERSION, True),
                  ("Python version", python_version(), True),
                  ("Discord.py version", discord_version(), True),
                  ("Uptime", uptime, True),
                  ("CPU time", cpu_time, True),
                  ("Memory usage", f"{mem_usage:,.3f} / {mem_total:,.0f} ({mem_of_total}%)", True),
                  ("Users", f"{self.bot.guild.member_count:,}", True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Misc(bot))