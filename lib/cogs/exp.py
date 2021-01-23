from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions, MissingPermissions
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
    
    @command(name="addxp", aliases=["+xp"])
    @has_permissions(administrator=True)
    async def add_xp_to_member(self, ctx, member: Member, amount: int):
        if member != ctx.author:
            db.execute("UPDATE exp SET XP = XP + ? WHERE UserID = ?", amount, member.id)
            db.commit()
            await ctx.send(f"I have added {amount} XP to {member.display_name}'s experience")
        else:
            await ctx.send("You can not add xp to yourself")
    
    @add_xp_to_member.error
    async def add_xp_to_member_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You are missing the required permissions to use this command")
        else:
            raise error
    
    @command(name="takexp", aliases=["-xp"])
    @has_permissions(administrator=True)
    async def remove_xp_to_member(self, ctx, member: Member, amount: int):
        if member != ctx.author:
            db.execute("UPDATE exp SET XP = XP - ? WHERE UserID = ?", amount, member.id)
            db.commit()
            await ctx.send(f"I have taken away {amount} XP from {member.display_name}'s experience")
        else:
            await ctx.send("You can not remove your own XP")
    
    @remove_xp_to_member.error
    async def remove_xp_to_member_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You are missing the required permissions to use this command")
        else:
            raise error

def setup(bot):
    bot.add_cog(exp(bot))