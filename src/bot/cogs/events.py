import disnake
from bot.ext import utils
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
