from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed
from datetime import datetime
from ..db import db #type: ignore

class ExampleCog(Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('ExampleCog')
        print('Example Cog loaded')
        await self.bot.stdout.send('Example cog loaded!')
    
    @Cog.listener()
    async def on_member_join(self, member):
        db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
    
    @Cog.listener()
    async def on_member_remove(self, member):
        db.execute("DELETE FROM exp WHERE UserID = ?", member.id)

def setup(bot):
    bot.add_cog(ExampleCog(bot))