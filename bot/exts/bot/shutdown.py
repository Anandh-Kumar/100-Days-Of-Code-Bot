# Copyright (c) 2022 AnandhKumar E S
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from discord.ext import commands, bridge
import discord
from time import gmtime, asctime


class ShutDown(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.is_owner()
    @bridge.bridge_command(name="shutdown", description="Shutdown bot.")
    async def _command(self, ctx):
        embed = discord.Embed(description=f"**`{self.bot.user}` is shutting down.**")
        current_time = asctime(gmtime())
        embed.set_footer(text=current_time)
        await ctx.send(embed=embed)
        exit()


def setup(bot: commands.Bot):
    bot.add_cog(ShutDown(bot))
