from typing import Optional

from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed, TextChannel
from datetime import datetime, timedelta
from random import sample

class Giveaway(Cog):

    def __init__(self, bot):
        self.bot = bot
        self.giveaways = []
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('Giveaway')
        print('Giveaway Cog loaded')
        await self.bot.stdout.send('Giveaway cog loaded!')
    
    @command(name="start",
             aliases=["giveawaystart", "startgiveaway", "sg", "gs"],
             brief="Starts a giveaway")
    async def begin_giveaway(self, ctx, channel: Optional[TextChannel], winners: int, hours: int, *, prize: str):
        '''Begins a giveaway for the set amount of winners, the set time and the prize.
        The time does have to be in seconds (in a future update it will be changed'''
        hours = hours * 3600 # Turns it from seconds into hours
        channel = channel or ctx.message.channel # If they don't define a channel, it will use the channel the message was sent in
        if winners > 0 and winners <= 5:
            embed = Embed(
                title=f"{prize.title()} giveaway",
                colour=0x0000FF, # Blue | Change it to whatever colour you want
                timestamp=datetime.utcnow())
        
            fields = [("Winners", str(winners), False),
                      ("End time:", f"{datetime.utcnow()+timedelta(seconds=hours*60)} UTC", False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
        
            message = await channel.send(embed=embed)
            await message.add_reaction("🎉")
        
            self.giveaways.append((channel.id, message.id, winners))

            self.bot.scheduler.add_job(self.complete_giveaway,
                                       "date",
                                       run_date=datetime.now()+timedelta(seconds=hours),
                                       args=[channel.id, message.id, int(winners),])
        else:
            embed = Embed(
                title="Giveaway error",
                description="I can't start a giveaway with that number of winners",
                colour=0xFF0000,
                timestamp=datetime.utcnow())
    
    async def complete_giveaway(self, channel_id, message_id, winner_limit: int):
        channel = self.bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)

        if len((entrants := [u for u in await message.reactions[0].users().flatten() if not u.bot])) > 0:
            if len(entrants) <= winner_limit:
                winners = entrants
            else:
                winners = sample(population=entrants, k=winner_limit)
            embed = Embed(
                title="Giveaway ended",
                description=f"[This giveaway]({message.jump_url}) has ened",
                colour=0x00FF00,
                timestamp=datetime.utcnow())
            await channel.send(embed=embed)
            for member in winners:
                await channel.send(f"{member.mention} has won the giveaway")
            self.giveaways.remove((channel_id, message.id, winner_limit)) #type: ignore

        else:
            await message.channel.send("Giveaway ended - no one entered!")
            self.giveaways.remove((channel_id, message.id, winner_limit))

def setup(bot):
    bot.add_cog(Giveaway(bot))