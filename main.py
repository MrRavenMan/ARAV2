import discord
import configparser
import time

from discord.ext import commands
from discord_components import DiscordComponents

from assigner import Assigner
from member_watch import MemberWatch


config = configparser.ConfigParser()
config.read("conf/config.ini")

intents = discord.Intents.default()
intents.members = True

TOKEN = config["General"]["TOKEN"]

client = commands.Bot(command_prefix='!', intents=intents)

client.add_cog(Assigner(client, config['Assigner']))
client.add_cog(MemberWatch(client, config['MemberWatch']))


@client.event
async def on_ready():
    print(f'{config["General"]["bot_name"]} has logged in as {client.user}')
    DiscordComponents(client)


@client.command(brief="Test if bot is online")  # Command to test if bot is online
@commands.has_role(config["General"]["manager_role"])
async def test(ctx):
    await ctx.message.channel.send('I am online :D')
    await ctx.message.delete()


@client.command(brief="Reload all config and description files")  # Command to reload all config and text files
@commands.has_role(config["General"]["manager_role"])
async def reload(ctx):
    config.read("conf/config.ini")
    client.remove_cog("Assigner")
    client.remove_cog("RoleWatcher")
    client.add_cog(Assigner(client, config['Assigner']))
    client.add_cog(MemberWatch(client, config['MemberWatch']))
    await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
    time.sleep(0.5)
    await ctx.message.delete()
    print("Reloading complete")


@client.command(aliases=["quit"], brief='Shut down bot')  # Command to shut down the bot
@commands.has_role(config["General"]["manager_role"])
async def close(ctx):
    await client.close()
    print("Bot shutting down")


@client.command(brief="Add role")
@commands.has_role(config["General"]["manager_role"])  # Add role using commmand
async def add_role(ctx, role: discord.Role, user: discord.Member):
    if ctx.author.guild_permissions.administrator:
        await user.add_roles(role)
        await ctx.send(f"Successfully given {role.mention} to {user.mention}.")
        print(f"Successfully given {role.mention} to {user.mention}.")


@client.command(brief="Removes role")
@commands.has_role(config["General"]["manager_role"])  # Remove role using commmand
async def remove_role(ctx, role: discord.Role, user: discord.Member):
    if ctx.author.guild_permissions.administrator:
        await user.remove_roles(role)
        await ctx.send(f"Successfully removed {role.mention} from {user.mention}.")
        print(f"Successfully removed {role.mention} from {user.mention}.")





""" RUN """
client.run(TOKEN)