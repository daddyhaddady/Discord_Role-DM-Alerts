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

import disnake

from bot import utils


class ConfigView(disnake.ui.View):
    """Adds a ui element with embed examples for each configured role
    and action buttons to navigate and edit an embed"""

    def __init__(self, embeds: list[disnake.Embed]):
        super().__init__(timeout=300)
        self.embeds = embeds
        self.current_index = 0

        self.previous.disabled = True

        for i, embed in enumerate(self.embeds, start=1):
            embed.set_footer(text=f"Viewing {i}/{len(self.embeds)} configured roles")

    @disnake.ui.button(label="\u200b", style=disnake.ButtonStyle.grey, disabled=True)
    async def first_slot(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        pass

    @disnake.ui.button(label="Previous", style=disnake.ButtonStyle.primary)
    async def previous(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):

        self.current_index -= 1
        self.next.disabled = False

        if self.current_index == 0:
            self.previous.disabled = True

        embed = self.embeds[self.current_index]
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="Next", style=disnake.ButtonStyle.primary)
    async def next(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):

        self.current_index += 1
        self.previous.disabled = False

        if self.current_index == len(self.embeds) - 1:
            self.next.disabled = True

        embed = self.embeds[self.current_index]
        await interaction.response.edit_message(embed=embed, view=self)

    @disnake.ui.button(label="\u200b", style=disnake.ButtonStyle.grey, disabled=True)
    async def last_slot(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        pass


class AddRole(disnake.ui.Modal):
    """Modal for adding a new role, with embed title and description"""

    def __init__(self, role: disnake.Role, data: dict):

        components = [
            disnake.ui.TextInput(
                label="Title",
                placeholder="You were given the {role} role in {guild}",
                custom_id="title",
                required=False,
                style=disnake.TextInputStyle.short,
                max_length=255,
            ),
            disnake.ui.TextInput(
                label="Message",
                placeholder="Using keys {guild} or {role} will be replaced with the guild and role names",
                custom_id="message",
                required=True,
                style=disnake.TextInputStyle.long,
                max_length=4000,
            ),
        ]

        super().__init__(title=f"Add {role.name}", components=components)
        self.role = role
        self.data = data

    async def callback(self, interaction: disnake.ModalInteraction):
        """Handles the callback for the submitted modal"""

        guild = interaction.guild

        # all checks passed, get title and message from modal
        title = (
            interaction.text_values.get("title")
            or "You were given the {role} role in {guild}"
        )
        message = interaction.text_values.get("message")

        # create the embed and store the new data
        embed = utils.create_dm_embed(
            guild, self.role, title, message, interaction.author
        )
        self.data[str(guild.id)].append(
            {"id": self.role.id, "title": title, "message": message}
        )
        utils.dump_config(self.data)

        await interaction.response.send_message(
            f"Config for {self.role.mention} has been added. Here is a preview!",
            embed=embed,
            ephemeral=True,
        )


class EditRole(disnake.ui.Modal):
    """Modal for adding a new role, with embed title and description"""

    def __init__(self, role: disnake.Role, data: dict):

        components = [
            disnake.ui.TextInput(
                label="Title",
                placeholder="You were given the {role} role in {guild}",
                custom_id="title",
                required=False,
                style=disnake.TextInputStyle.short,
                max_length=255,
            ),
            disnake.ui.TextInput(
                label="Message",
                placeholder="Using keys {guild} or {role} will be replaced with the guild and role names",
                custom_id="message",
                required=True,
                style=disnake.TextInputStyle.long,
                max_length=4000,
            ),
        ]

        super().__init__(title=f"Editing {role.name}", components=components)
        self.role = role
        self.data = data

    async def callback(self, interaction: disnake.ModalInteraction):
        """Handles the callback for the submitted modal"""

        guild = interaction.guild
        roles = self.data[str(guild.id)]

        for role in roles:
            if role["id"] == self.role.id:
                role = role

        # all checks passed, get title and message from modal
        title = (
            interaction.text_values.get("title")
            or "You were given the {role} role in {guild}"
        )
        message = interaction.text_values.get("message")

        # create the embed and store the new data
        embed = utils.create_dm_embed(
            guild, self.role, title, message, interaction.author
        )

        role["title"] = title
        role["message"] = message
        utils.dump_config(self.data)

        await interaction.response.send_message(
            f"Config for {self.role.mention} has been added. Here is a preview!",
            embed=embed,
            ephemeral=True,
        )
