import json
import time
import configparser

from discord.ext import commands
from discord import utils, Embed, Colour, File
from discord_components import Button, ButtonStyle, InteractionType, component

config = configparser.ConfigParser()
config.read("conf/config.ini")
owner = config["General"]["manager_role"]


class Assigner(commands.Cog):
    def __init__(self, client, config):
        self.bot = client
        self.config = config
        with open('conf/roles.json') as json_file:
            self.roles = json.load(json_file)

    async def role_assign(self, ctx, res, role_name, manager_role):  # Function for assigning a member a role
        member = await ctx.channel.guild.fetch_member((res.user.id))
        role = utils.get(member.guild.roles, name=role_name)
        if role not in member.roles:
            await member.add_roles(role)
            print(f"{member.name} has been assigned the role of {res.component.label}")
            return 1
        else:
            return 0

    async def role_unassign(self, ctx, res, role_name):  # Function for unassigning a member a role
        member = await ctx.channel.guild.fetch_member((res.user.id))
        role = utils.get(member.guild.roles, name=role_name)
        if role in member.roles:
            await member.remove_roles(role)
            print(f"{member.name} has been unassigned the role of {res.component.label}")
            return 2
        else:
            return 0

    async def role_invert(self, ctx, res, role_name):  # Function for inverting (assigning/unassigning a mebmer a role)
        member = await ctx.channel.guild.fetch_member((res.user.id))
        role = utils.get(member.guild.roles, name=role_name)
        if role not in member.roles:
            await member.add_roles(role)
            print(f"{member.name} has been assigned the role of {res.component.label}")
            return 1
        elif role in member.roles:
            await member.remove_roles(role)
            print(f"{member.name} has been unassigned the role of {res.component.label}")
            return 2
        else:
            return 0

    
    async def role_func(self, ctx, button_inf):
        print(f'Adding button for {button_inf["role_name"]}')
        if button_inf["active"] is True:
            join = Button(style=ButtonStyle.green, label=button_inf["lbl_join"], id=button_inf["emb_join"])
            leave = Button(style=ButtonStyle.red, label=button_inf["lbl_leave"], id=button_inf["emb_leave"])
        
            await ctx.send(
                "\n **This role is for {0} of the community** \n".format(utils.get(ctx.guild.roles, name=button_inf["role_name"]).mention),
                components=[
                    [join, leave]
                ]
            )
            await ctx.message.delete()


    @commands.Cog.listener()  # Remove unused role commands on startup
    async def on_ready(self):
        for x in range(1, 21):
            if self.roles[f"Role{x}"]["active"] is False:
                self.bot.remove_command(f"role{x}")


    @commands.command(brief=f'Buttons for assigning/unassigning Role 1')
    @commands.has_role(owner)
    async def roles(self, ctx):
        role_list = "The available roles are: \n"
        for role_num, _ in self.roles.items():
            if self.roles[role_num]["active"] is True:
                role_list += f'*{role_num} = {self.roles[role_num]["role_name"]}\n'

        await ctx.message.reply(role_list)
        await ctx.message.delete()

    @commands.command(brief="Posts introduction message for role buttons")
    @commands.has_role(owner)
    async def role_intro(self, ctx):
        if self.config["role_introduction"] == "True":
            with open ("conf/role_intro.txt", "r") as myfile:
                data=myfile.readlines()

            text = ""
            for i in data:
                text += i

            await ctx.send(text, file=File(self.config["role_introduction_picture"]))
            await ctx.message.delete()


    @commands.command(brief=f'Buttons for assigning/unassigning all roles with one click')
    @commands.has_role(owner)
    async def role_all(self, ctx):  # Button for picking all roles with one click
        join = Button(style=ButtonStyle.blue, label="Assign All Roles", id="e_all_join")
        leave = Button(style=ButtonStyle.red, label="Unassign All Roles", id="e_all_leave")


        await ctx.send(
            f"__**Pick your new role!**__ \n \
            \n **This button is for assigning all roles of the community** \n",
            components=[
                [join, leave]
            ]
        )
        await ctx.message.delete()

        # _ = await ctx.invoke(self.bot.get_command("role1"))


    """ Commands for all roles in roles list"""
    # Non active roles will not do anything other than load the next role
    @commands.command(brief=f'Buttons for assigning/unassigning Role 1')
    @commands.has_role(owner)
    async def role1(self, ctx):
        await self.role_func(ctx, self.roles["Role1"])
        # _ = await ctx.invoke(self.bot.get_command("role2"))

    @commands.command(brief=f'Buttons for assigning/unassigning Role 2')
    @commands.has_role(owner)
    async def role2(self, ctx):
        await self.role_func(ctx, self.roles["Role2"])
        # _ = await ctx.invoke(self.bot.get_command("role3"))

    @commands.command(brief=f'Buttons for assigning/unassigning Role 3')
    @commands.has_role(owner)
    async def role3(self, ctx):
        await self.role_func(ctx, self.roles["Role3"])
        # _ = await ctx.invoke(self.bot.get_command("role4"))

    @commands.command(brief=f'Buttons for assigning/unassigning Role 4')
    @commands.has_role(owner)
    async def role4(self, ctx):
        await self.role_func(ctx, self.roles["Role4"])
        # _ = await ctx.invoke(self.bot.get_command("role5"))

    @commands.command(brief=f'Buttons for assigning/unassigning Role 5')
    @commands.has_role(owner)
    async def role5(self, ctx):
        await self.role_func(ctx, self.roles["Role5"])
        # _ = await ctx.invoke(self.bot.get_command("role6"))

    @commands.command(brief=f'Buttons for assigning/unassigning Role 6')
    @commands.has_role(owner)
    async def role6(self, ctx):
        await self.role_func(ctx, self.roles["Role6"])
        # _ = await ctx.invoke(self.bot.get_command("role7"))

    @commands.command(brief=f'Buttons for assigning/unassigning Role 7')
    @commands.has_role(owner)
    async def role7(self, ctx):
        await self.role_func(ctx, self.roles["Role7"])
        # _ = await ctx.invoke(self.bot.get_command("role8"))

    @commands.command(brief=f'Buttons for assigning/unassigning Role 8')
    @commands.has_role(owner)
    async def role8(self, ctx):
        await self.role_func(ctx, self.roles["Role8"])
        # _ = await ctx.invoke(self.bot.get_command("role9"))

    @commands.command(brief=f'Buttons for assigning/unassigning Role 9')
    @commands.has_role(owner)
    async def role9(self, ctx):
        await self.role_func(ctx, self.roles["Role9"])
        # _ = await ctx.invoke(self.bot.get_command("role10"))

    @commands.command(brief=f'Buttons for assigning/unassigning Role 10')
    @commands.has_role(owner)
    async def role10(self, ctx):
        await self.role_func(ctx, self.roles["Role10"])
        # _ = await ctx.invoke(self.bot.get_command("role11"))

    @commands.command(brief=f'Buttons for assigning/unassigning Role 11')
    @commands.has_role(owner)
    async def role11(self, ctx):
        await self.role_func(ctx, self.roles["Role11"])
        # _ = await ctx.invoke(self.bot.get_command("role12"))

    @commands.command(brief=f'Buttons for assigning/unassigning Role 12')
    @commands.has_role(owner)
    async def role12(self, ctx):
        await self.role_func(ctx, self.roles["Role12"])
        # _ = await ctx.invoke(self.bot.get_command("role13"))

    @commands.command(brief=f'Buttons for assigning/unassigning Role 13')
    @commands.has_role(owner)
    async def role13(self, ctx):
        await self.role_func(ctx, self.roles["Role13"])
        # _ = await ctx.invoke(self.bot.get_command("role14"))

    @commands.command(brief=f'Buttons for assigning/unassigning Role 14')
    @commands.has_role(owner)
    async def role14(self, ctx):
        await self.role_func(ctx, self.roles["Role14"])
        # _ = await ctx.invoke(self.bot.get_command("role15"))

    @commands.command(brief=f'Buttons for assigning/unassigning Role 15')
    @commands.has_role(owner)
    async def role15(self, ctx):
        await self.role_func(ctx, self.roles["Role15"])
        # _ = await ctx.invoke(self.bot.get_command("role16"))

    @commands.command(brief=f'Buttons for assigning/unassigning Role 16')
    @commands.has_role(owner)
    async def role16(self, ctx):
        await self.role_func(ctx, self.roles["Role16"])
        # _ = await ctx.invoke(self.bot.get_command("role17"))

    @commands.command(brief=f'Buttons for assigning/unassigning Role 17')
    @commands.has_role(owner)
    async def role17(self, ctx):
        await self.role_func(ctx, self.roles["Role17"])
        # _ = await ctx.invoke(self.bot.get_command("role18"))

    @commands.command(brief=f'Buttons for assigning/unassigning Role 18')
    @commands.has_role(owner)
    async def role18(self, ctx):
        await self.role_func(ctx, self.roles["Role18"])
        # _ = await ctx.invoke(self.bot.get_command("role19"))

    @commands.command(brief=f'Buttons for assigning/unassigning Role 19')
    @commands.has_role(owner)
    async def role19(self, ctx):
        await self.role_func(ctx, self.roles["Role19"])
        # _ = await ctx.invoke(self.bot.get_command("role20"))

    @commands.command(brief=f'Buttons for assigning/unassigning Role 20')
    @commands.has_role(owner)
    async def role20(self, ctx):
        await self.role_func(ctx, self.roles["Role20"])
        print("Loading role buttons complete")


    @commands.command(brief="Makes all the role buttons work and function")
    @commands.has_role(owner)
    async def buttons_on(self, ctx):  # Watches all roles for button_click state updates
        e_all_join = Embed(title="All roles assigned", description="You have joined all roles!", colour=Colour.from_rgb(50, 50, 50))
        e_all_leave = Embed(title="All roles unassigned", description="You have been unassigned all roles!", colour=Colour.from_rgb(50, 50, 50))
        
        buttons = {  # Make buttons for join all and leave all buttons
            "e_all_join": e_all_join,
            "e_all_leave": e_all_leave           
            }

        if self.roles["Role1"]["active"] is True: # if Role1 is set to active in roles.json make embeds for button
            e_R1_join = Embed(title=f'{(self.roles["Role1"]["role_name"])} Role assigned',
                                    description=self.roles["Role1"]["embed"]["desc_join"],
                                    colour=Colour.from_rgb(self.roles["Role1"]["embed"]["color_join_r"],
                                    self.roles["Role1"]["embed"]["color_join_g"],
                                    self.roles["Role1"]["embed"]["color_join_b"]))
            e_R1_leave = Embed(title=f'{self.roles["Role1"]["role_name"]} Role unassigned',
                                    description=self.roles["Role1"]["embed"]["desc_leave"],
                                    colour=Colour.from_rgb(self.roles["Role1"]["embed"]["color_leave_r"],
                                    self.roles["Role1"]["embed"]["color_leave_g"],
                                    self.roles["Role1"]["embed"]["color_leave_b"]))
            buttons["e_R1_join"] = e_R1_join
            buttons["e_R1_leave"] = e_R1_leave

        if self.roles["Role2"]["active"] is True:
            e_R2_join = Embed(title=f'{self.roles["Role2"]["role_name"]} Role assigned',
                                    description=self.roles["Role2"]["embed"]["desc_join"],
                                    colour=Colour.from_rgb(self.roles["Role2"]["embed"]["color_join_r"],
                                    self.roles["Role2"]["embed"]["color_join_g"],
                                    self.roles["Role2"]["embed"]["color_join_b"]))
            e_R2_leave = Embed(title=f'{self.roles["Role2"]["role_name"]} Role unassigned',
                                    description=self.roles["Role2"]["embed"]["desc_leave"],
                                    colour=Colour.from_rgb(self.roles["Role2"]["embed"]["color_leave_r"],
                                    self.roles["Role2"]["embed"]["color_leave_g"],
                                    self.roles["Role2"]["embed"]["color_leave_b"]))
            buttons["e_R2_join"] = e_R2_join
            buttons["e_R2_leave"] = e_R2_leave

        if self.roles["Role3"]["active"] is True:
            e_R3_join = Embed(title=f'{self.roles["Role3"]["role_name"]} Role assigned',
                                    description=self.roles["Role3"]["embed"]["desc_join"],
                                    colour=Colour.from_rgb(self.roles["Role3"]["embed"]["color_join_r"],
                                    self.roles["Role3"]["embed"]["color_join_g"],
                                    self.roles["Role3"]["embed"]["color_join_b"]))
            e_R3_leave = Embed(title=f'{self.roles["Role3"]["role_name"]} Role unassigned',
                                    description=self.roles["Role3"]["embed"]["desc_leave"],
                                    colour=Colour.from_rgb(self.roles["Role3"]["embed"]["color_leave_r"],
                                    self.roles["Role3"]["embed"]["color_leave_g"],
                                    self.roles["Role3"]["embed"]["color_leave_b"]))
            buttons["e_R3_join"] = e_R3_join
            buttons["e_R3_leave"] = e_R3_leave

        if self.roles["Role4"]["active"] is True:
            e_R4_join = Embed(title=f'{self.roles["Role4"]["role_name"]} Role assigned',
                                    description=self.roles["Role4"]["embed"]["desc_join"],
                                    colour=Colour.from_rgb(self.roles["Role4"]["embed"]["color_join_r"],
                                    self.roles["Role4"]["embed"]["color_join_g"],
                                    self.roles["Role4"]["embed"]["color_join_b"]))
            e_R4_leave = Embed(title=f'{self.roles["Role4"]["role_name"]} Role unassigned',
                                    description=self.roles["Role4"]["embed"]["desc_leave"],
                                    colour=Colour.from_rgb(self.roles["Role4"]["embed"]["color_leave_r"],
                                    self.roles["Role4"]["embed"]["color_leave_g"],
                                    self.roles["Role4"]["embed"]["color_leave_b"]))
            buttons["e_R4_join"] = e_R4_join
            buttons["e_R4_leave"] = e_R4_leave

        if self.roles["Role5"]["active"] is True:
            e_R5_join = Embed(title=f'{self.roles["Role5"]["role_name"]} Role assigned',
                                    description=self.roles["Role5"]["embed"]["desc_join"],
                                    colour=Colour.from_rgb(self.roles["Role5"]["embed"]["color_join_r"],
                                    self.roles["Role5"]["embed"]["color_join_g"],
                                    self.roles["Role5"]["embed"]["color_join_b"]))
            e_R5_leave = Embed(title=f'{self.roles["Role5"]["role_name"]} Role unassigned',
                                    description=self.roles["Role5"]["embed"]["desc_leave"],
                                    colour=Colour.from_rgb(self.roles["Role5"]["embed"]["color_leave_r"],
                                    self.roles["Role5"]["embed"]["color_leave_g"],
                                    self.roles["Role5"]["embed"]["color_leave_b"]))
            buttons["e_R5_join"] = e_R5_join
            buttons["e_R5_leave"] = e_R5_leave

        if self.roles["Role5"]["active"] is True:      # To increase performance, roles are divided into 5 role groups
            if self.roles["Role6"]["active"] is True:  # where is active checks are first performed on sets of 5
                e_R6_join = Embed(title=f'{self.roles["Role6"]["role_name"]} Role assigned',
                                        description=self.roles["Role6"]["embed"]["desc_join"],
                                        colour=Colour.from_rgb(self.roles["Role6"]["embed"]["color_join_r"],
                                        self.roles["Role6"]["embed"]["color_join_g"],
                                        self.roles["Role6"]["embed"]["color_join_b"]))
                e_R6_leave = Embed(title=f'{self.roles["Role6"]["role_name"]} Role unassigned',
                                        description=self.roles["Role6"]["embed"]["desc_leave"],
                                        colour=Colour.from_rgb(self.roles["Role6"]["embed"]["color_leave_r"],
                                        self.roles["Role6"]["embed"]["color_leave_g"],
                                        self.roles["Role6"]["embed"]["color_leave_b"]))
                buttons["e_R6_join"] = e_R6_join
                buttons["e_R6_leave"] = e_R6_leave

            if self.roles["Role7"]["active"] is True:
                e_R7_join = Embed(title=f'{self.roles["Role7"]["role_name"]} Role assigned',
                                        description=self.roles["Role7"]["embed"]["desc_join"],
                                        colour=Colour.from_rgb(self.roles["Role7"]["embed"]["color_join_r"],
                                        self.roles["Role7"]["embed"]["color_join_g"],
                                        self.roles["Role7"]["embed"]["color_join_b"]))
                e_R7_leave = Embed(title=f'{self.roles["Role7"]["role_name"]} Role unassigned',
                                        description=self.roles["Role7"]["embed"]["desc_leave"],
                                        colour=Colour.from_rgb(self.roles["Role7"]["embed"]["color_leave_r"],
                                        self.roles["Role7"]["embed"]["color_leave_g"],
                                        self.roles["Role7"]["embed"]["color_leave_b"]))
                buttons["e_R7_join"] = e_R7_join
                buttons["e_R7_leave"] = e_R7_leave

            if self.roles["Role8"]["active"] is True:
                e_R8_join = Embed(title=f'{self.roles["Role8"]["role_name"]} Role assigned',
                                        description=self.roles["Role8"]["embed"]["desc_join"],
                                        colour=Colour.from_rgb(self.roles["Role8"]["embed"]["color_join_r"],
                                        self.roles["Role8"]["embed"]["color_join_g"],
                                        self.roles["Role8"]["embed"]["color_join_b"]))
                e_R8_leave = Embed(title=f'{self.roles["Role8"]["role_name"]} Role unassigned',
                                        description=self.roles["Role8"]["embed"]["desc_leave"],
                                        colour=Colour.from_rgb(self.roles["Role8"]["embed"]["color_leave_r"],
                                        self.roles["Role8"]["embed"]["color_leave_g"],
                                        self.roles["Role8"]["embed"]["color_leave_b"]))
                buttons["e_R8_join"] = e_R8_join
                buttons["e_R8_leave"] = e_R8_leave

            if self.roles["Role9"]["active"] is True:
                e_R9_join = Embed(title=f'{self.roles["Role9"]["role_name"]} Role assigned',
                                        description=self.roles["Role9"]["embed"]["desc_join"],
                                        colour=Colour.from_rgb(self.roles["Role9"]["embed"]["color_join_r"],
                                        self.roles["Role9"]["embed"]["color_join_g"],
                                        self.roles["Role9"]["embed"]["color_join_b"]))
                e_R9_leave = Embed(title=f'{self.roles["Role9"]["role_name"]} Role unassigned',
                                        description=self.roles["Role9"]["embed"]["desc_leave"],
                                        colour=Colour.from_rgb(self.roles["Role9"]["embed"]["color_leave_r"],
                                        self.roles["Role9"]["embed"]["color_leave_g"],
                                        self.roles["Role9"]["embed"]["color_leave_b"]))

            if self.roles["Role10"]["active"] is True:
                e_R10_join = Embed(title=f'{self.roles["Role10"]["role_name"]} Role assigned',
                                        description=self.roles["Role10"]["embed"]["desc_join"],
                                        colour=Colour.from_rgb(self.roles["Role10"]["embed"]["color_join_r"],
                                        self.roles["Role10"]["embed"]["color_join_g"],
                                        self.roles["Role10"]["embed"]["color_join_b"]))
                e_R10_leave = Embed(title=f'{self.roles["Role10"]["role_name"]} Role unassigned',
                                        description=self.roles["Role10"]["embed"]["desc_leave"],
                                        colour=Colour.from_rgb(self.roles["Role10"]["embed"]["color_leave_r"],
                                        self.roles["Role10"]["embed"]["color_leave_g"],
                                        self.roles["Role10"]["embed"]["color_leave_b"]))

        if self.roles["Role11"]["active"] is True:      # To increase performance, roles are divided into 5 role groups
            if self.roles["Role11"]["active"] is True:  # where is active checks are first performed on sets of 5
                e_R11_join = Embed(title=f'{self.roles["Role11"]["role_name"]} Role assigned',
                                        description=self.roles["Role11"]["embed"]["desc_join"],
                                        colour=Colour.from_rgb(self.roles["Role1"]["embed"]["color_join_r"],
                                        self.roles["Role11"]["embed"]["color_join_g"],
                                        self.roles["Role11"]["embed"]["color_join_b"]))
                e_R11_leave = Embed(title=f'{self.roles["Role11"]["role_name"]} Role unassigned',
                                        description=self.roles["Role11"]["embed"]["desc_leave"],
                                        colour=Colour.from_rgb(self.roles["Role11"]["embed"]["color_leave_r"],
                                        self.roles["Role11"]["embed"]["color_leave_g"],
                                        self.roles["Role11"]["embed"]["color_leave_b"]))

            if self.roles["Role12"]["active"] is True:
                e_R12_join = Embed(title=f'{self.roles["Role2"]["role_name"]} Role assigned',
                                        description=self.roles["Role2"]["embed"]["desc_join"],
                                        colour=Colour.from_rgb(self.roles["Role2"]["embed"]["color_join_r"],
                                        self.roles["Role2"]["embed"]["color_join_g"],
                                        self.roles["Role2"]["embed"]["color_join_b"]))
                e_R12_leave = Embed(title=f'{self.roles["Role2"]["role_name"]} Role unassigned',
                                        description=self.roles["Role2"]["embed"]["desc_leave"],
                                        colour=Colour.from_rgb(self.roles["Role2"]["embed"]["color_leave_r"],
                                        self.roles["Role2"]["embed"]["color_leave_g"],
                                        self.roles["Role2"]["embed"]["color_leave_b"]))
            
            if self.roles["Role13"]["active"] is True:
                e_R13_join = Embed(title=f'{self.roles["Role13"]["role_name"]} Role assigned',
                                        description=self.roles["Role13"]["embed"]["desc_join"],
                                        colour=Colour.from_rgb(self.roles["Role13"]["embed"]["color_join_r"],
                                        self.roles["Role13"]["embed"]["color_join_g"],
                                        self.roles["Role13"]["embed"]["color_join_b"]))
                e_R13_leave = Embed(title=f'{self.roles["Role13"]["role_name"]} Role unassigned',
                                        description=self.roles["Role13"]["embed"]["desc_leave"],
                                        colour=Colour.from_rgb(self.roles["Role13"]["embed"]["color_leave_r"],
                                        self.roles["Role13"]["embed"]["color_leave_g"],
                                        self.roles["Role13"]["embed"]["color_leave_b"]))

            if self.roles["Role4"]["active"] is True:
                e_R14_join = Embed(title=f'{self.roles["Role14"]["role_name"]} Role assigned',
                                        description=self.roles["Role14"]["embed"]["desc_join"],
                                        colour=Colour.from_rgb(self.roles["Role14"]["embed"]["color_join_r"],
                                        self.roles["Role14"]["embed"]["color_join_g"],
                                        self.roles["Role14"]["embed"]["color_join_b"]))
                e_R14_leave = Embed(title=f'{self.roles["Role14"]["role_name"]} Role unassigned',
                                        description=self.roles["Role14"]["embed"]["desc_leave"],
                                        colour=Colour.from_rgb(self.roles["Role14"]["embed"]["color_leave_r"],
                                        self.roles["Role14"]["embed"]["color_leave_g"],
                                        self.roles["Role14"]["embed"]["color_leave_b"]))

            if self.roles["Role15"]["active"] is True:
                e_R15_join = Embed(title=f'{self.roles["Role15"]["role_name"]} Role assigned',
                                        description=self.roles["Role15"]["embed"]["desc_join"],
                                        colour=Colour.from_rgb(self.roles["Role15"]["embed"]["color_join_r"],
                                        self.roles["Role15"]["embed"]["color_join_g"],
                                        self.roles["Role15"]["embed"]["color_join_b"]))
                e_R15_leave = Embed(title=f'{self.roles["Role15"]["role_name"]} Role unassigned',
                                        description=self.roles["Role15"]["embed"]["desc_leave"],
                                        colour=Colour.from_rgb(self.roles["Role5"]["embed"]["color_leave_r"],
                                        self.roles["Role15"]["embed"]["color_leave_g"],
                                        self.roles["Role15"]["embed"]["color_leave_b"]))

        if self.roles["Role16"]["active"] is True:      # To increase performance, roles are divided into 5 role groups
            if self.roles["Role16"]["active"] is True:  # where is active checks are first performed on sets of 5
                e_R16_join = Embed(title=f'{self.roles["Role16"]["role_name"]} Role assigned',
                                        description=self.roles["Role16"]["embed"]["desc_join"],
                                        colour=Colour.from_rgb(self.roles["Role16"]["embed"]["color_join_r"],
                                        self.roles["Role16"]["embed"]["color_join_g"],
                                        self.roles["Role16"]["embed"]["color_join_b"]))
                e_R16_leave = Embed(title=f'{self.roles["Role16"]["role_name"]} Role unassigned',
                                        description=self.roles["Role16"]["embed"]["desc_leave"],
                                        colour=Colour.from_rgb(self.roles["Role6"]["embed"]["color_leave_r"],
                                        self.roles["Role16"]["embed"]["color_leave_g"],
                                        self.roles["Role16"]["embed"]["color_leave_b"]))

            if self.roles["Role17"]["active"] is True:
                e_R17_join = Embed(title=f'{self.roles["Role17"]["role_name"]} Role assigned',
                                        description=self.roles["Role17"]["embed"]["desc_join"],
                                        colour=Colour.from_rgb(self.roles["Role17"]["embed"]["color_join_r"],
                                        self.roles["Role17"]["embed"]["color_join_g"],
                                        self.roles["Role17"]["embed"]["color_join_b"]))
                e_R17_leave = Embed(title=f'{self.roles["Role17"]["role_name"]} Role unassigned',
                                        description=self.roles["Role17"]["embed"]["desc_leave"],
                                        colour=Colour.from_rgb(self.roles["Role7"]["embed"]["color_leave_r"],
                                        self.roles["Role17"]["embed"]["color_leave_g"],
                                        self.roles["Role17"]["embed"]["color_leave_b"]))

            if self.roles["Role18"]["active"] is True:
                e_R18_join = Embed(title=f'{self.roles["Role18"]["role_name"]} Role assigned',
                                        description=self.roles["Role18"]["embed"]["desc_join"],
                                        colour=Colour.from_rgb(self.roles["Role8"]["embed"]["color_join_r"],
                                        self.roles["Role18"]["embed"]["color_join_g"],
                                        self.roles["Role18"]["embed"]["color_join_b"]))
                e_R18_leave = Embed(title=f'{self.roles["Role18"]["role_name"]} Role unassigned',
                                        description=self.roles["Role18"]["embed"]["desc_leave"],
                                        colour=Colour.from_rgb(self.roles["Role8"]["embed"]["color_leave_r"],
                                        self.roles["Role18"]["embed"]["color_leave_g"],
                                        self.roles["Role18"]["embed"]["color_leave_b"]))

            if self.roles["Role19"]["active"] is True:
                e_R19_join = Embed(title=f'{self.roles["Role19"]["role_name"]} Role assigned',
                                        description=self.roles["Role19"]["embed"]["desc_join"],
                                        colour=Colour.from_rgb(self.roles["Role9"]["embed"]["color_join_r"],
                                        self.roles["Role19"]["embed"]["color_join_g"],
                                        self.roles["Role19"]["embed"]["color_join_b"]))
                e_R19_leave = Embed(title=f'{self.roles["Role19"]["role_name"]} Role unassigned',
                                        description=self.roles["Role19"]["embed"]["desc_leave"],
                                        colour=Colour.from_rgb(self.roles["Role9"]["embed"]["color_leave_r"],
                                        self.roles["Role19"]["embed"]["color_leave_g"],
                                        self.roles["Role19"]["embed"]["color_leave_b"]))

            if self.roles["Role20"]["active"] is True:
                e_R20_join = Embed(title=f'{self.roles["Role20"]["role_name"]} Role assigned',
                                        description=self.roles["Role20"]["embed"]["desc_join"],
                                        colour=Colour.from_rgb(self.roles["Role20"]["embed"]["color_join_r"],
                                        self.roles["Role20"]["embed"]["color_join_g"],
                                        self.roles["Role20"]["embed"]["color_join_b"]))
                e_R20_leave = Embed(title=f'{self.roles["Role20"]["role_name"]} Role unassigned',
                                        description=self.roles["Role20"]["embed"]["desc_leave"],
                                        colour=Colour.from_rgb(self.roles["Role20"]["embed"]["color_leave_r"],
                                        self.roles["Role20"]["embed"]["color_leave_g"],
                                        self.roles["Role20"]["embed"]["color_leave_b"]))


        print("Watching all buttons")  # Confirm watching
        await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
        time.sleep(0.5)
        await ctx.message.delete()


        while True:
            event = await self.bot.wait_for("button_click")
            if event.channel is not ctx.channel:
                return
            if event.channel == ctx.channel:
                response = buttons.get(event.component.id)

                if event.component.id == 'e_all_join':
                    member = await ctx.channel.guild.fetch_member((event.user.id))
                    role_list = []
                    
                    for role_num, _ in self.roles.items():
                        if self.roles[role_num]["active"] is True:
                            role = utils.get(member.guild.roles, name=self.roles[role_num]["role_name"])
                            if role not in member.roles:
                                role_list.append(role)
                    
                    await member.add_roles(*role_list)
                elif event.component.id == 'e_all_leave':
                    member = await ctx.channel.guild.fetch_member((event.user.id))
                    role_list = []
                    for role_num, _ in self.roles.items():
                        #  resp = await self.role_unassign(ctx, event, self.roles[key]["role_name"])
                        if self.roles[role_num]["active"] is True:
                            role = utils.get(member.guild.roles, name=self.roles[role_num]["role_name"])
                            if role in member.roles:
                                role_list.append(role)
                    
                    await member.remove_roles(*role_list)

                
                if event.component.id == "e_R1_join":
                    resp = await self.role_assign(ctx, event, self.roles["Role1"]["role_name"])
                elif event.component.id == "e_R1_leave":
                    resp = await self.role_unassign(ctx, event, self.roles["Role1"]["role_name"])
                elif event.component.id == "e_R2_join":
                    resp = await self.role_assign(ctx, event, self.roles["Role2"]["role_name"])
                elif event.component.id == "e_R2_leave":
                    resp = await self.role_unassign(ctx, event, self.roles["Role2"]["role_name"])
                elif event.component.id == "e_R3_join":
                    resp = await self.role_assign(ctx, event, self.roles["Role3"]["role_name"])
                elif event.component.id == "e_R3_leave":
                    resp = await self.role_unassign(ctx, event, self.roles["Role3"]["role_name"])
                elif event.component.id == "e_R4_join":
                    resp = await self.role_assign(ctx, event, self.roles["Role4"]["role_name"])
                elif event.component.id == "e_R4_leave":
                    resp = await self.role_unassign(ctx, event, self.roles["Role4"]["role_name"])
                elif event.component.id == "e_R5_join":
                    resp = await self.role_assign(ctx, event, self.roles["Role5"]["role_name"])
                elif event.component.id == "e_R5_leave":
                    resp = await self.role_unassign(ctx, event, self.roles["Role5"]["role_name"])

                if self.roles["Role6"]["active"] is True:  # To increase performance, roles are divided into 5 role groups
                    if event.component.id == "e_R6_join":  # where is active checks are first performed on sets of 5
                        resp = await self.role_assign(ctx, event, self.roles["Role6"]["role_name"])
                    elif event.component.id == "e_R6_leave":
                        resp = await self.role_unassign(ctx, event, self.roles["Role6"]["role_name"])
                    elif event.component.id == "e_R7_join":
                        resp = await self.role_assign(ctx, event, self.roles["Role7"]["role_name"])
                    elif event.component.id == "e_R7_leave":
                        resp = await self.role_unassign(ctx, event, self.roles["Role7"]["role_name"])
                    elif event.component.id == "e_R8_join":
                        resp = await self.role_assign(ctx, event, self.roles["Role8"]["role_name"])
                    elif event.component.id == "e_R8_leave":
                        resp = await self.role_unassign(ctx, event, self.roles["Role8"]["role_name"])
                    elif event.component.id == "e_R9_join":
                        resp = await self.role_assign(ctx, event, self.roles["Role9"]["role_name"])
                    elif event.component.id == "e_R9_leave":
                        resp = await self.role_unassign(ctx, event, self.roles["Role9"]["role_name"])
                    elif event.component.id == "e_R10_join":
                        resp = await self.role_assign(ctx, event, self.roles["Role10"]["role_name"])
                    elif event.component.id == "e_R10_leave":
                        resp = await self.role_unassign(ctx, event, self.roles["Role10"]["role_name"])

                if self.roles["Role11"]["active"] is True:  # To increase performance, roles are divided into 5 role groups
                    if event.component.id == "e_R11_join":  # where is active checks are first performed on sets of 5
                        resp = await self.role_assign(ctx, event, self.roles["Role11"]["role_name"])
                    elif event.component.id == "e_R11_leave":
                        resp = await self.role_unassign(ctx, event, self.roles["Role11"]["role_name"])
                    elif event.component.id == "e_R12_join":
                        resp = await self.role_assign(ctx, event, self.roles["Role12"]["role_name"])
                    elif event.component.id == "e_R12_leave":
                        resp = await self.role_unassign(ctx, event, self.roles["Role12"]["role_name"])
                    elif event.component.id == "e_R13_join":
                        resp = await self.role_assign(ctx, event, self.roles["Role13"]["role_name"])
                    elif event.component.id == "e_R13_leave":
                        resp = await self.role_unassign(ctx, event, self.roles["Role13"]["role_name"])
                    elif event.component.id == "e_R14_join":
                        resp = await self.role_assign(ctx, event, self.roles["Role14"]["role_name"])
                    elif event.component.id == "e_R14_leave":
                        resp = await self.role_unassign(ctx, event, self.roles["Role14"]["role_name"])
                    elif event.component.id == "e_R15_join":
                        resp = await self.role_assign(ctx, event, self.roles["Role15"]["role_name"])
                    elif event.component.id == "e_R15_leave":
                        resp = await self.role_unassign(ctx, event, self.roles["Role15"]["role_name"])

                if self.roles["Role16"]["active"] is True:  # To increase performance, roles are divided into 5 role groups
                    if event.component.id == "e_R16_join":  # where is active checks are first performed on sets of 5
                        resp = await self.role_assign(ctx, event, self.roles["Role16"]["role_name"])
                    elif event.component.id == "e_R16_leave":
                        resp = await self.role_unassign(ctx, event, self.roles["Role16"]["role_name"])
                    elif event.component.id == "e_R17_join":
                        resp = await self.role_assign(ctx, event, self.roles["Role17"]["role_name"])
                    elif event.component.id == "e_R17_leave":
                        resp = await self.role_unassign(ctx, event, self.roles["Role17"]["role_name"])
                    elif event.component.id == "e_R18_join":
                        resp = await self.role_assign(ctx, event, self.roles["Role18"]["role_name"])
                    elif event.component.id == "e_R18_leave":
                        resp = await self.role_unassign(ctx, event, self.roles["Role18"]["role_name"])
                    elif event.component.id == "e_R19_join":
                        resp = await self.role_assign(ctx, event, self.roles["Role19"]["role_name"])
                    elif event.component.id == "e_R19_leave":
                        resp = await self.role_unassign(ctx, event, self.roles["Role19"]["role_name"])
                    elif event.component.id == "e_R20_join":
                        resp = await self.role_assign(ctx, event, self.roles["Role20"]["role_name"])
                    elif event.component.id == "e_R20_leave":
                        resp = await self.role_unassign(ctx, event, self.roles["Role20"]["role_name"])


                if response is None:  # check for error in response from button or resp from role assigner func
                    await event.channel.send(
                        "Something went wrong. Please try it again"
                    )

                if event.channel == ctx.channel:  # respond to user with response
                    await event.respond(
                        type=InteractionType.ChannelMessageWithSource,
                        embed=response
                    )
