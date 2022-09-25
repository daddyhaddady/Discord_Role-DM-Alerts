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
from disnake.ext import commands


class Events(commands.Cog):
    """Add role based event listeners to the bot"""

    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog loaded: {self.qualified_name}")

    @commands.Cog.listener()
    async def on_member_update(self, before: disnake.Member, after: disnake.Member):
        """
        Disnake.on_member_update event listener

        Event Actions
        -------------
        Send a DM to the member after a role has been granted, if
        that role is one that has a custom message enabled

        Parameters
        ----------
        before: :class:`disnake.Member`
            the cached member data from before the update
        after: :class:`disnake.Member`
            the cached member data after the update
        """

        guild = before.guild

        if len(after.roles) < len(before.roles):
            # a role was taken away, we only care if role were added
            return

        guild_roles = utils.get_guild_roles(guild, after)

        if guild_roles == [] or not guild_roles:
            # the guild has not setup any configurations yet
            return

        new_role_id = list(set(after.roles) - set(before.roles))[0].id

        for role in guild_roles:
            if not new_role_id == role.id:
                continue

            # role matches a configured role
            # tries to send DM to the user - if user has privacy settings enabled
            # bot quietly handles the error
            try:
                await after.send(embed=role.embed)
            except disnake.Forbidden:
                return


def setup(bot: commands.InteractionBot):
    bot.add_cog(Events(bot))
