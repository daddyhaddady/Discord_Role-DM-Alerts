"""
MIT License

Copyright (c) 2022 DLCHAMP

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from typing import Optional

import disnake
from bot import utils, views
from disnake.ext import commands


class Admin(commands.Cog):
    """Add admin commands and listeners to bot"""

    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
        self.admin_role = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog loaded: {self.qualified_name}")

    @commands.slash_command(name="config")
    async def config(self, interaction: disnake.AppCmdInter):
        """Parent command - always invoked with subcommands"""
        pass

    @config.sub_command(name="view")
    async def config_view(
        self, interaction: disnake.AppCmdInter, role_name: Optional[str] = None
    ):
        """View the current DM message for all roles, or specify a role to view

        Parameters
        ----------
        role: :class:`disnake.Role`
            Optional role you wish to view the current message for
        """
        if role_name == "No roles have been configured":
            return await interaction.response.send_message(
                "No roles have been configured for this guild", ephemeral=True
            )

        guild = interaction.guild
        guild_roles = utils.get_guild_roles(guild, interaction.author)

        # if a role name is passed, check if that role exists in the guild
        if role_name and not disnake.utils.get(guild.roles, name=role_name):
            return await interaction.response.send_message(
                f"There are no roles in this guild named {role_name}. please check your spelling and try again "
                "or don't include a role to see all roles currently configured.",
                ephemeral=True,
            )

        # guild has no configured roles, or the guild has not been configured yet
        if guild_roles == [] or not guild_roles:
            return await interaction.response.send_message(
                "There are currently no roles configured for this guild. Add a role message with </:>.",
                ephemeral=True,
            )

        if role_name:
            role = [role for role in guild_roles if role.name == role_name][0]
            return await interaction.response.send_message(
                f"Here is the current configuration for the <@&{role.id}> role",
                embed=role.embed,
                ephemeral=True,
            )

        embeds = [role.embed for role in guild_roles]
        if len(embeds) == 1:
            view = disnake.utils.MISSING
            message = "This is the only role you have configured so far\n\u200b"

        else:
            view = views.ConfigView(embeds)
            message = "Here are you configured roles. Use the buttons navigate through each role to view an example\n\u200b"

        await interaction.response.send_message(
            message, embed=embeds[0], ephemeral=True, view=view
        )

    @config.sub_command(name="add")
    async def config_add(self, interaction: disnake.AppCmdInter, role: disnake.Role):
        """Add a new role and message to the config

        Parameters
        ----------
        role: :class:`disnake.Role`
            A role you wish to view the current message for
        """

        guild = interaction.guild
        data = utils.load_data()

        # if guild has no config yet, add it
        if not str(guild.id) in data:
            data[str(guild.id)] = []

        # check if the role being added is already configured
        roles = [role["id"] for role in data[str(guild.id)]]
        if role.id in roles:
            return await interaction.response.send_message(
                f"This role has already been configured", ephemeral=True
            )

        modal = views.AddRole(role, data)

        await interaction.response.send_modal(modal=modal)

    @config.sub_command(name="remove")
    async def config_remove(self, interaction: disnake.AppCmdInter, role_name: str):
        """Remove a role from the config

        Parameters
        ----------
        role: :class:`str`
            The name of the role you wish to remove
        """
        if role_name == "No roles have been configured":
            return await interaction.response.send_message(
                "No roles have been configured for this guild", ephemeral=True
            )

        guild = interaction.guild
        data = utils.load_data()

        # check if the guild has any config data
        if not str(guild.id) in data:
            return await interaction.response.send_message(
                "This guild does not have a configuration yet", ephemeral=True
            )

        guild_data: list[dict] = data[str(guild.id)]

        # check that the role exists
        role = disnake.utils.get(guild.roles, name=role_name)
        if not role:
            return await interaction.response.send_message(
                f"{role_name} does not exist in {guild.name}.", ephemeral=True
            )

        # check if the role exists in config data
        for guild_role in guild_data:
            if role.id == guild_role["id"]:

                guild_data.remove(guild_role)
                utils.dump_config(data)

                return await interaction.response.send_message(
                    f"{role.name} was removed from the config", ephemeral=True
                )

        return await interaction.response.send_message(
            f"{role.name} has not been configured.", ephemeral=True
        )

    @config.sub_command(name="edit")
    async def config_edit(self, interaction: disnake.AppCmdInter, role_name: str):
        """Edit a a configured role

        Parameters
        ----------
        role: :class:`str`
            The name of the role you wish to remove
        """
        if role_name == "No roles have been configured":
            return await interaction.response.send_message(
                "No roles have been configured for this guild", ephemeral=True
            )

        guild = interaction.guild
        data = utils.load_data()

        # check if the guild has any config data
        if not str(guild.id) in data:
            return await interaction.response.send_message(
                "This guild does not have a configuration yet", ephemeral=True
            )

        guild_data: list[dict] = data[str(guild.id)]

        # check that the role exists
        role = disnake.utils.get(guild.roles, name=role_name)
        if not role:
            return await interaction.response.send_message(
                f"{role_name} does not exist in {guild.name}.", ephemeral=True
            )

        # check if the role exists in config data
        if not role.id in [role["id"] for role in guild_data]:
            return await interaction.response.send_message(
                f"{role.name} has not been configured yet. Please add it to the config before trying to edit it",
                ephemeral=True,
            )

        modal = views.EditRole(role, data)
        await interaction.response.send_modal(modal=modal)

    @config_view.autocomplete("role_name")
    @config_remove.autocomplete("role_name")
    @config_edit.autocomplete("role_name")
    async def config_view_autocomplete(
        self, interaction: disnake.AppCmdInter, string: str
    ):
        string = string.lower()
        roles = utils.get_guild_roles(interaction.guild, interaction.author)
        if not roles or roles == []:
            return ["No roles have been configured"]

        return [role.name for role in roles if string in role.name.lower()]


def setup(bot: commands.InteractionBot):
    bot.add_cog(Admin(bot))
