from discord import Forbidden
from discord.ext.commands import Cog

class MemberWatch(Cog):
    def __init__(self, client, config):
        self.bot = client
        self.config = config

    @Cog.listener()
    async def on_ready(self):
        print("Member Watch: ON")

    @Cog.listener()
    async def on_member_join(self, member):
        print("member joined")
        await self.bot.get_channel(int(self.config["join_msg_channel_id"])).send(f"{member.mention} has joined the server!")

        try:
            with open ("conf/welcome_dm.txt", "r") as myfile:
                data=myfile.readlines()
            text = ""
            for i in data:
                text += i
            await member.send(text.format(user_mention=member.guild.name))
        except Forbidden:
            pass


    @Cog.listener()
    async def on_member_remove(self, member):
        print("member left")
        await self.bot.get_channel(int(self.config["leave_msg_channel_id"])).send(f"**{member.name}#{member.discriminator}** has left the server!")

    
