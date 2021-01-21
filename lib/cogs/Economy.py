from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed, Member
from datetime import datetime
from random import randint
from typing import Optional
import sqlite3
from sqlite3 import Error

class Economy(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command()
    async def bal(self, ctx, member: Optional[Member]):
        author = member or ctx.author

        await ctx.send(f'Hello {author.mention}')

def setup(bot):
    bot.add_cog(Economy(bot))