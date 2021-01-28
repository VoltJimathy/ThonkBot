from ..db import db
from datetime import datetime
from asyncio import sleep
from glob import glob
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Intents
from discord import Embed, DMChannel
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import when_mentioned_or, command, has_permissions
from discord.ext.commands import CommandNotFound, CommandOnCooldown, MissingRequiredArgument, BadArgument, MissingRole

OWNER_IDS = [700336923264155719]
COGS = [path.split("\\")[-1][:-3] for path in glob('./lib/cogs/*.py')]

def get_prefix(bot, message):
    prefix = db.field("SELECT Prefix FROM Guilds WHERE GuildID = ?", message.guild.id)
    return when_mentioned_or(prefix)(bot, message)

class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)
    
    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f'{cog} cog ready!')
    
    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
    def __init__(self):
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler) #type: ignore

        super().__init__(
            command_prefix=get_prefix,
            owner_ids=OWNER_IDS,
            intents=Intents.all()
            )
    def setup(self):
        for cog in COGS:
            self.load_extension(f'lib.cogs.{cog}')
            print(f'{cog} cog loaded!')
        print('Setup complete!')

    def update_db(self):
        db.multiexec("INSERT OR IGNORE INTO Guilds (GuildID) VALUES (?)",
                     ((guild.id,) for guild in self.guilds))
        
        db.multiexec("INSERT OR IGNORE INTO exp (UserID) VALUES (?)",
					 ((member.id,) for member in self.guild.members if not member.bot))

        db.multiexec("INSERT OR IGNORE INTO Mod (UserId) VALUES (?)",
                     ((member.id,) for member in self.guild.members if not member.bot))
        
        to_remove = []
        stored_members = db.column("SELECT UserID FROM exp")
        for id_ in stored_members:
            if not self.guild.get_member(id_):
                to_remove.append(id_)
                
        db.multiexec("DELETE FROM exp WHERE UserID = ?",
			         ((id_,) for id_ in to_remove))

        to_remove = []
        stored_members = db.column("SELECT UserID FROM Mod")
        for id_ in stored_members:
            if not self.guild.get_member(id_):
                to_remove.append(id_)

        db.multiexec("DELETE FROM Mod WHERE UserId = ?",
                     ((id_) for id_ in to_remove))
        
        db.commit()

    def run(self, version):
        self.VERSION = version

        print(f'running setup in version {version}...')
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()
        
        print("Running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print('Bot connected!')

    async def on_disconnect(self):
        print('Bot disconnected!')

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong!")
        await self.stdout.send("An error occured!")
        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass

        elif isinstance(exc, CommandOnCooldown):
            embed = Embed(
            	title="__Cooldown__",
            	description=f"You are on cooldown for {exc.retry_after:,.2f} seconds. Try again when the cooldows is over",
            	colour=0xDD2222,
            	timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
        
        elif isinstance(exc, MissingRequiredArgument):
            embed = Embed(
                title="__Error__",
                description="You are missing a required argument in that command",
                colour=0xFF0000,
                timestamp=datetime.utcnow())
            await ctx.send(embed=embed)

        elif isinstance(exc, BadArgument):
            embed = Embed(
                title="__Error__",
                description="You are using a bad argument",
                colour=0xFF0000,
                timestamp=datetime.utcnow())
            await ctx.send(embed=embed)

        elif isinstance(exc, MissingRole):
            pass

        elif hasattr(exc, "original"):
            raise exc.original
        else:
            raise exc
    
    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(777500671922012170)
            self.stdout = self.get_channel(782694805720662026)
            self.scheduler.start()

            await self.stdout.send('Now online!')
            self.update_db()

            embed = Embed(title='__Now online!__', description='Thonk Bot is now online!', timestamp=datetime.utcnow())
            embed.add_field(name="Now Online!", value="I am now online and ready to be used!", inline=True)
            embed.set_footer(text="This is a footer!")
            embed.set_author(name="Thonk Bot", icon_url=self.user.avatar_url)
            embed.set_thumbnail(url=self.guild.icon_url)
            await self.stdout.send(embed=embed)

            while not self.cogs_ready.all_ready():
                await sleep(0.1)

            print("Bot ready!")
            self.ready= True

        else:
            print("Bot reconnected!")

    async def on_message(self, message):
        if not message.author.bot:
            if isinstance(message.channel, DMChannel):
                embed = Embed(
                    title="Modmail",
                    colour=message.author.colour,
                    timestamp=datetime.utcnow())
                embed.set_thumbnail(url=message.author.avatar_url)
                fields = [("Member", message.author.display_name, False),
                          ("Message", message.content, False)]
            else:
                await self.process_commands(message)


bot = Bot()