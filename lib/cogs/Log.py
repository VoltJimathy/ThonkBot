from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command
from datetime import datetime
from ..db import db #type: ignore

class Log(Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.MemberUpdateChannel = self.bot.get_channel(777500673419902995)
            self.bot.cogs_ready.ready_up('Log')
        print('Log loaded')
        await self.bot.stdout.send('Log cog loaded!')

    @Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            embed = Embed(
                title="Member update",
                description=f"Username change",
                timestamp=datetime.utcnow())
            embed.set_thumbnail(url=after.avatar_url) #type: ignore
            fields = [("Before", before.name, False),
                      ("After", after.name, False)]
            
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await self.MemberUpdateChannel.send(embed=embed)
        if before.discriminator != after.discriminator:
            embed = Embed(
                title="Member update",
                description=f"Discriminator change",
                timestamp=datetime.utcnow())
            embed.set_thumbnail(url=after.avatar_url)
            fields = [("Before", before.discriminator, False),
                      ("After", after.discriminator, False)]
            
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await self.MemberUpdateChannel.send(embed=embed)
        if before.avatar_url != after.avatar_url:
            embed = Embed(
                title="Member update",
                description=f"Avatar change (Below is the new avatar, to the right is the old avatar)",
                timestamp=datetime.utcnow())
            embed.set_thumbnail(url=before.avatar_url)
            embed.set_image(url=after.avatar_url)
            await self.MemberUpdateChannel.send(embed=embed)

    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            embed = Embed(
                title="Member update",
                description=f"Nickname change",
                colour=after.colour,
                timestamp=datetime.utcnow())
            embed.set_thumbnail(url=after.avatar_url)
            fields = [("Before", before.display_name, False),
                      ("After", after.display_name, False)]
            
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await self.MemberUpdateChannel.send(embed=embed)
        if before.roles != after.roles:
            embed = Embed(
                title="Member update",
                description=f"Role updates",
                colour=after.colour,
                timestamp=datetime.utcnow())
            embed.set_thumbnail(url=after.avatar_url)
            fields = [("Before", ", ".join([r.mention for r in before.roles]), False),
                      ("After", ", ".join([r.mention for r in after.roles]), False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await self.MemberUpdateChannel.send(embed=embed)

    @Cog.listener()
    async def on_raw_message_edit(self, payload):
        #print(payload)
        message_id=payload.message_id
        data = payload.data
        channel = self.bot.get_channel(int(data["channel_id"]))
        guild=channel.guild
        before= payload.cached_message
        after = await channel.fetch_message(message_id)
        if not after.author.bot:
            embed = Embed(
                title="Message update",
                description=f"**__Message edit:__**\n\n**Channel:** {channel.mention}\n**Author:** {after.author.mention}",
                colour=after.author.colour,
                timestamp=datetime.utcnow())
            embed.set_thumbnail(url=after.author.avatar_url)
            fields = [("Before", before.content, False),
                      ("After", after.content, False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await self.MemberUpdateChannel.send(embed=embed)

    @Cog.listener()
    async def on_raw_message_delete(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        message = payload.cached_message
        embed = Embed(
            title="Message update",
            description=f"Message delete",
            colour=message.author.colour,
            timestamp=datetime.utcnow())
        embed.set_thumbnail(url=message.author.avatar_url)
        fields = [("Message", message.content, False)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await self.MemberUpdateChannel.send(embed=embed)

def setup(bot):
    bot.add_cog(Log(bot))
