from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions, CheckFailure
from discord import Embed
from datetime import datetime
from ..db import db # type: ignore

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

def setup(bot):
    bot.add_cog(Misc(bot))