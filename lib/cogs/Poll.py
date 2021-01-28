from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed
from datetime import datetime

numbers = ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣",
		   "6⃣", "7⃣", "8⃣", "9⃣", "🔟")

class Poll(Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('Poll')
        print('Poll Cog loaded')
        await self.bot.stdout.send('Poll cog loaded!')

    @command(name="createpoll", aliases=["mkpoll"])
    async def create_poll(self, ctx, question, *options):
        if len(options) <= 10:
            embed = Embed(title="Poll",
                description=question,
                colour=ctx.author.colour,
                timestamp=datetime.utcnow())

            fields = [("Options", "\n".join([f"{numbers[idx]} {option}" for idx, option in enumerate(options)]), False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            message = await ctx.send(embed=embed)
            for emoji in numbers[:len(options)]:
                await message.add_reaction(emoji)
        else:
            await ctx.send("You can't have more than 10 options")



def setup(bot):
    bot.add_cog(Poll(bot))