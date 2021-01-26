from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed
from datetime import datetime

class Reactions(Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('Reactions')
        print('Reaction Cog loaded')
        await self.bot.stdout.send('Reaction cog loaded!')
    
    @Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # This event will only fire if the message is in the bots cache
        # For this one you can use the 'reaction' as a reaction object
        # You can also use the user object as the person who reacted
        pass

    @Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        # This event will only fire if the message is in the bots cache
        # For this one you can use the 'reaction' as a reaction object
        # You can also use the user object as the person who reacted
        pass

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # This event will fire, even if the message isn't in the bots cache
        # The only argument for this event (other than self) is payload
        # The payload for adding a reaction has a member object instead
        # This makes it easier to do some things with it
        # If you want to see everything in the payload, do the following line
        # print(payload)
        pass

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # This event will fire, even if the message isn't in the bots cache
        # The only argument for this event (other than self) is payload
        # The payload for this event does not have a member object
        # However you can get the member object by using the following line
        member = self.bot.guild.get_member(payload.user_id)
        # If you want to see everything in the payload, do the following line
        # print(payload)
        pass

def setup(bot):
    bot.add_cog(Reactions(bot)) #type: ignore