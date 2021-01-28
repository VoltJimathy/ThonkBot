from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown
from discord import Embed
from datetime import datetime
from random import randint
import pybelieva
from typing import Optional

class unb(Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        self.unb_client = pybelieva.Client('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBfaWQiOiI3OTQxNzc0NjUwNDg0OTk0NTYiLCJpYXQiOjE2MDk0MTcwNjJ9.tynjkExkZ1r1g-zILaK9EvHz9Y5P5lP9JDC9znjOYSY')
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('unb')
        print('unb loaded')
        await self.bot.stdout.send('unb Cog loaded!')
    
    @command()
    @cooldown(1, 60, BucketType.user)
    async def books(self, ctx):
        '''Gives money for reading books'''
        cash = randint(100, 500)
        await self.unb_client.patch_user_balance(ctx.guild.id, ctx.author.id, cash=cash)
        embed = Embed(
            title="Book Command",
            description=f'You just got {cash} money for reading books!',
            colour=0x00ff00,
            timestamp=datetime.utcnow())
        await ctx.send(embed=embed)
    
    @command()
    @cooldown(1, 3600, BucketType.user)
    async def hourly(self, ctx):
        '''Gives you a random number of money between 1K and 2K for waiting 1 hour'''
        cash = randint(1000, 2000)
        await self.unb_client.patch_user_balance(ctx.guild.id, ctx.author.id, cash=cash)
        embed = Embed(
            title="Hourly",
            description=f"You just got {cash} for waiting 1 hour. I wonder who gave it to you",
            colour=0x00ff00,
            timestamp=datetime.utcnow())
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(unb(bot))