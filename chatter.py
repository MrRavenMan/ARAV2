from discord import Forbidden
from discord.ext.commands import Cog
from discord.channel import DMChannel

import random
import json


class Chatter(Cog):
    def __init__(self, client, config):
        self.bot = client
        self.config = config

        # load chats.json file
        with open('conf/Chatter_conf/chats.json') as chats_file:
            chats_data = json.load(chats_file)
            self.chats = chats_data["chats"]
            self.always_respond_to_role_ids = chats_data["always_respond_to_role_ids"]

        # map chat calls to index of chats
        self.calls = []
        self.calls_map = []

        for i, chat in enumerate(self.chats):
            for call in chat["call"]:
                self.calls.append(call)
                self.calls_map.append(i)


    @Cog.listener()
    async def on_ready(self):
        print("Chatter: ON")
        print(f"Chatter contains {len(self.chats)} different chats")


    @Cog.listener()
    async def on_message(self, message):
        messageAuthor = message.author
        
        if message.content.lower() in self.calls:
            idx = self.calls.index(message.content.lower())
            chat_idx = self.calls_map[idx]
            
            # If always respond is disabled and user not in specified role, only respond if probability True
            if self.config["always_respond"] == "False" and not any(role.id in self.always_respond_to_role_ids for role in messageAuthor.roles): 
                i = 1 - random.uniform(0, 1) 
                k = float(self.chats[chat_idx]["probability"])
                if i > k:
                    return
                
            response = random.choice(self.chats[chat_idx]["response"])
            await message.channel.send(response.format(user_mention=messageAuthor.name,
                                            server_mention=messageAuthor.guild.name))

        

