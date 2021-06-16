import discord
import requests
import json
import configparser

from discord.ext import commands
from discord_components import DiscordComponents

from assigner import Assigner
from member_watch import MemberWatch


TOKEN = "ODUzNjYzNDQ1MTUzMjE4NTgw.YMYqCQ.qVyNMvyuyvQ9OA4wleEnZ8QH8Fo"

config = configparser.ConfigParser()
config.read("conf/config.ini")

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

client.add_cog(Assigner(client, config['Assigner']))
client.add_cog(MemberWatch(client, config['MemberWatch']))


def get_quote():
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        return quote
        


@client.event
async def on_ready():
    print(f'ARA has logged in as {client.user}')
    DiscordComponents(client)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!ARA'):
        if message.content.startswith('!ARA.help'):
            await message.channel.send('Type !ARA.test to test if I am online \n Type !ARA.quote to get some inspiration')

        elif message.content.startswith('!ARA.test'):
            await message.channel.send('I am online :D')

        elif message.content.startswith('!ARA.quote'):
            quote = get_quote()
            await message.channel.send(quote)
    await client.process_commands(message)


@client.command(aliases=["quit"])
@commands.has_role(config["General"]["manager_role"])
async def close(ctx):
    await client.close()
    print("Bot shutting down")


@client.command()
@commands.has_role(config["General"]["manager_role"])
async def add_role(ctx, role: discord.Role, user: discord.Member):
    if ctx.author.guild_permissions.administrator:
        await user.add_roles(role)
        await ctx.send(f"Successfully given {role.mention} to {user.mention}.")

@client.command()
@commands.has_role(config["General"]["manager_role"])
async def remove_role(ctx, role: discord.Role, user: discord.Member):
    if ctx.author.guild_permissions.administrator:
        await user.remove_roles(role)
        await ctx.send(f"Successfully removed {role.mention} from {user.mention}.")





""" RUN """
client.run(TOKEN)