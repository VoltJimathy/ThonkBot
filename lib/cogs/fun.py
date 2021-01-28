from random import choice
import random
from discord.ext.commands import Cog
from discord.ext.commands import command
from datetime import datetime
from discord import Embed
from aiohttp import request

class Fun(Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @command(name="hello", aliases=["h", "hola", "hi"])
    async def say_hello(self, ctx):
        await ctx.send(f'{choice(("Hello", "Hi", "Hey", "Hola"))} {ctx.author.mention}!')
    
    @command(name="dice", aliases=["role"])
    async def roll_dice(self, ctx, die_string: str):
        '''This command is temporarily dissabled'''
        #dice, value = (int(term) for term in die_string.split("d"))
        #roles = [random.randint(1, value) for i in range(dice)]
        await ctx.send("This command is currently dissabled")
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('fun')
        print('Fun cog loaded')
        await self.bot.stdout.send('Fun cog loaded!')
    
    @command(name="meme", aliases=["sm", "sendmeme", "Meme", "SendMeme"])
    async def Sendmeme(self, ctx):
        '''Sends a random meme from the ```https://some-random-api.ml/meme``` API'''
        URL = "https://some-random-api.ml/meme"

        async with request("GET", URL) as response:
            if response.status == 200:
                data = await response.json()
                embed = Embed(
                    title=data["caption"],
                    colour=0x0000ff,
                    timestamp=datetime.utcnow())
                embed.set_image(url=data["image"])
                await ctx.send(embed=embed)
            else:
                await ctx.send(f'API returned a {response.status} status')

    @command(name="fact")
    async def animal_fact(self, ctx, animal: str):
        '''Sends a fact about a specified animal.
        The animals you can use are:
        `dog`, `cat`, `panda`, `fox`, `bird`, and `koala`'''
        if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
            fact_url = f"https://some-random-api.ml/facts/{animal}"
            image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

            async with request("GET", image_url) as response:
                if response.status == 200:
                    data = await response.json()
                    image_link = data["link"]
                else:
                    embed = Embed(
                        title="API error",
                        description=f"The API being used for the image returned a {response.status} status",
                        colour=0xFF0000,
                        timestamp=datetime.utcnow())
                    await ctx.send(embed=embed)

            async with request("GET", fact_url) as response:
                if response.status == 200:
                    data = await response.json()
                    embed = Embed(
                        title=f"{animal.title()} fact",
                        description=data["fact"],
                        colour=ctx.author.colour,
                        timestamp=datetime.utcnow())
                    embed.set_image(url=image_link)
                    await ctx.send(embed=embed)
                else:
                    embed = Embed(
                        title="API error",
                        description=f"The API being used for the fact returned a {response.status} status",
                        colour=0xFF0000,
                        timestamp=datetime.utcnow())
                    await ctx.send(embed=embed)
        else:
            embed = Embed(
                title="Invalid Animal",
                description="No facts are available for that animal unfortantly",
                colour=0xFF0000,
                timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
    
    @command(name="8ball", aliases=["8Ball", "8b", "8B"])
    async def ball_8(self, ctx, *, question):
        '''Ask our magic 8 ball a question!'''
        replies = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "It is certain.", "It is decidedly so."]
        embed = Embed(
            title='**8 Ball**',
            colour = 0x0000ff
        )
        embed.add_field(name="Question:", value=question, inline=False)
        embed.add_field(name="Answer:", value=choice(replies), inline=False)
        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Fun(bot))