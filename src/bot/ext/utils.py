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

import json
from dataclasses import dataclass
from typing import Optional

import disnake


@dataclass
class Role:
    id: int
    name: str
    guild: disnake.Guild
    embed: disnake.Embed


def load_data() -> dict:
    """Load all data from config.json"""
    with open("./bot/config.json") as f:
        return json.load(f)


def get_guild_roles(guild: disnake.Guild, member: disnake.Member) -> list[Role]:
    """Returns a list of Role dataclass objects for each role/message
    in the guild's config"""

    data = load_data()
    if not str(guild.id) in data:
        return

    guild_data = data[str(guild.id)]
    roles = []

    for item in guild_data:
        _id = item["id"]
        _title = item["title"]
        _message = item["message"]

        _role = guild.get_role(_id)
        embed = create_dm_embed(guild, _role, _title, _message, member)

        roles.append(Role(id=_id, name=_role.name, guild=guild, embed=embed))

    return roles


def dump_config(data: dict) -> None:
    """Dumps the updated config back to config.json"""
    with open("./bot/config.json", "w") as f:
        json.dump(data, f, indent=4)


def create_dm_embed(
    guild: disnake.Guild,
    role: disnake.Role,
    title: str,
    message: str,
    member: disnake.Member,
) -> disnake.Embed:
    """Create the embed for the passed role and return it"""

    embed = disnake.Embed(
        title=format_str(title, guild=guild, role=role, member=member),
        description=format_str(
            message, guild=guild, role=role, member=member, mention=True
        ),
    )
    embed.set_thumbnail(url=guild.icon.url if guild.icon else disnake.Embed.Empty)

    return embed


def format_str(
    string: str,
    *,
    guild: Optional[disnake.Guild] = None,
    role: Optional[disnake.Role] = None,
    member: Optional[disnake.Member] = None,
    mention: Optional[bool] = False,
) -> str:
    """Formats the title or message str by replacing variables with discord object attributes
    then returns the formatted string"""

    if guild:
        string = string.replace("{guild}", guild.name)

    if role:
        string = string.replace("{role}", role.name if not mention else role.mention)

    if member:
        string = string.replace(
            "{member}", member.name if not mention else member.mention
        )

    return string
