from typing import Optional

from discord.utils import get
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.menus import MenuPages, ListPageSource
from discord import Embed
from datetime import datetime

def syntax(command):
    cmd_and_aliases = " | ".join([str(command), *command.aliases])
    params = []

    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")
    params = " ".join(params)

    return f"`{cmd_and_aliases} {params}`"

class HelpMenu(ListPageSource):

    def __init__(self, ctx, data):
        self.ctx = ctx
        self.data = data
        super().__init__(data, per_page=5)

    async def write_page(self, menu, fields=[]):
        offset = (menu.current_page*self.per_page) + 1
        len_data = len(self.entries)

        embed = Embed(
            title="Help",
            description="Welcome to the ThonkBot help command!",
            colour=0x0000FF,
            timestamp=datetime.utcnow())
        embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
        embed.set_footer(text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} commands.")

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed

    async def format_page(self, menu, entries):
        fields = []

        for entry in entries:
            fields.append((entry.brief or "No description", syntax(entry)))

        return await self.write_page(menu, fields)

class Help(Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('Help')
        print('Help Cog loaded')
        await self.bot.stdout.send('Help cog loaded!')

    async def cmd_help(self, ctx, command):
        embed = Embed(
            title=f"{command} help",
            description=syntax(command),
            colour=0x0000FF,
            timestamp=datetime.utcnow())
        embed.add_field(name="Command Description", value=command.help, inline=False)
        await ctx.send(embed=embed)

    @command(name="help")
    async def show_help(self, ctx, cmd: Optional[str]):
        """Shows this help command"""
        if cmd == None:
            menu = MenuPages(
                source=HelpMenu(ctx, list(self.bot.commands)),
                delete_message_after=True,
                timeout=9999999.0)
            
            await menu.start(ctx)
        else:
            if (command := get(self.bot.commands, name=cmd)):
                await self.cmd_help(ctx, command)
            else:
                embed = Embed(
                    title="Invalid command",
                    description=f"The command {command} can not be found",
                    colour=0xFF0000,
                    timestamp=datetime.utcnow())
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))