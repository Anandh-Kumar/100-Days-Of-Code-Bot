# Copyright (c) 2022 AnandhKumar E S
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from discord.ext import commands, bridge
import discord
import typing
from bot.bot import Bot


class SetChannel(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    @bridge.bridge_command(
        name="100daysofcode", description="Set channel for 100DaysOfCode."
    )
    async def _100_command(
        self,
        ctx: typing.Union[commands.Context, discord.ApplicationContext],
        channel: discord.TextChannel,
    ):
        channel_id = channel.id
        guild_id = ctx.guild_id

        old_channel_id = await self.bot.mongo.set_channel(
            guild_id, "100DaysOfCode", channel_id
        )

        embed = discord.Embed(
            description=f"Changed channel (`{old_channel_id}` -> `{channel_id}`)."
        )
        if isinstance(ctx, commands.Context):
            await ctx.send(embed=embed)
        elif isinstance(ctx, discord.ApplicationContext):
            await ctx.respond(embed=embed)

    @bridge.bridge_command(
        name="bot_updates", description="Set channel for bot updates."
    )
    async def _bot_updates_command(
        self,
        ctx: typing.Union[commands.Context, discord.ApplicationContext],
        channel: discord.TextChannel,
    ):
        channel_id = channel.id
        guild_id = ctx.guild_id

        old_channel_id = await self.bot.mongo.set_channel(
            guild_id, "bot_updates", channel_id
        )

        embed = discord.Embed(
            description=f"Changed channel (`{old_channel_id}` -> `{channel_id}`)."
        )
        if isinstance(ctx, commands.Context):
            await ctx.send(embed=embed)
        elif isinstance(ctx, discord.ApplicationContext):
            await ctx.respond(embed=embed)


def setup(bot: Bot):
    bot.add_cog(SetChannel(bot))
