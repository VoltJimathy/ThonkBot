from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed, Member
from datetime import datetime, timedelta
from random import randint
from ..db import db #type: ignore
from typing import Optional

class exp(Cog):

    def __init__(self, bot):
        self.bot = bot
    
    async def process_xp(self, message):
        xp, lvl, xplock = db.record("SELECT XP, Level, XPLock FROM exp WHERE UserID = ?", message.author.id)

        if datetime.utcnow() > datetime.fromisoformat(xplock):
            await self.add_xp(message, xp, lvl)
    
    async def add_xp(self, message, xp, level):
        xp_to_add = randint(10, 20)
        new_lvl = int(((xp + xp_to_add)//100) ** 0.55)

        db.execute("UPDATE exp SET XP = XP + ?, Level = ?, XPLock = ? WHERE UserID = ?",
                   xp_to_add, new_lvl, (datetime.utcnow()+timedelta(seconds=5)).isoformat(), message.author.id)
        
        if new_lvl > level:
            await message.channel.send(f"Congratulations {message.author.mention}, you have just leveled up to {new_lvl:,}")


    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('exp')
        print('exp Cog loaded')
        await self.bot.stdout.send('exp cog loaded!')
    
    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            await self.process_xp(message)
    
    @command(name="rank", aliases=["r"])
    async def rank(self, ctx, member: Optional[Member]):
        member = member or ctx.author

        xp, level = db.record("SELECT XP, Level FROM exp WHERE UserID = ?", member.id,)

        embed = Embed(
            title=f"{member.display_name}'s rank",
            colour=member.colour,
            timestamp=datetime.utcnow())
        fields = [("Level", level, True),
                  ("XP", xp, True)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(exp(bot))