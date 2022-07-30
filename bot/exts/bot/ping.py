# Copyright (c) 2022 AnandhKumar E S
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from discord.ext import commands, bridge
import discord


class Ping(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @bridge.bridge_command(name="ping", description="shows bot latency.")
    async def _command(self, ctx):
        latency = round(self.bot.latency * 1000, 2)

        # Gets color according to latency
        if latency <= 40:
            latency_color = discord.Color.green()
        elif latency <= 100:
            latency_color = discord.Color.orange()
        else:
            latency_color = discord.Color.red()

        embed = discord.Embed(description=f"**Pong!** {latency}ms", color=latency_color)

        if isinstance(ctx, discord.ApplicationContext):
            await ctx.respond(embed=embed)
        elif isinstance(ctx, commands.Context):
            await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Ping(bot))
