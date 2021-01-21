from typing import Optional
from time import time
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed
from datetime import datetime
from asyncio import sleep

class TestCog(Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('TestCog')
        print('TestCog loaded')
        await self.bot.stdout.send('Test Cog Loaded!')

    @command(name="timer")
    async def timer(self, ctx, time: int):
        orr_time = time
        msg = await ctx.send(f"You have started a timer for {time} seconds")
        while time > 0:
            time -= 1
            await sleep(1)
            await msg.edit(content=f"You have {time} left on your {orr_time} second timer")
        await ctx.send(f'{ctx.author.mention}, your {orr_time} second timer has ended!')

    @command(name="Reminder")
    async def Reminder(self, ctx, time: int, *, message: Optional[str] = "No message"):
        embed = Embed(
            title=f"__Reminder for {ctx.author.display_name}:__",
            description=message,
            colour=0x0000ff,
            timestamp=datetime.utcnow())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(f"You have started a reminder that ends in {time} seconds")
        while time > 0:
            await sleep(1)
            time -= 1
        await ctx.send(f'{ctx.author.mention}:', embed=embed)
    
    @command(name="ping")
    async def ping(self, ctx):
        start = time() #type: ignore
        message = await ctx.send(f"Pong! Bot Latency: {self.bot.latency*1000:,.0f} ms")
        end = time()

        await message.edit(content=f"Pong! Bot Latency: {self.bot.latency*1000:,.0f} ms. Response time: {(end-start)*1000:,.0f} ms.")

def setup(bot):
    bot.add_cog(TestCog(bot))