# Copyright (c) 2022 AnandhKumar E S
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from discord.ext import commands
from discord.ext.commands import Cog
from pathlib import Path


class Bot(commands.Bot):
    def __init__(self, command_prefix=..., **options):
        super().__init__(command_prefix, **options)
        self.load_all_extensions()

    @Cog.listener()
    async def on_ready(self):
        print(self.user)

    def load_all_extensions(self):
        """Load every extensions from each category inside exts(folder)."""

        path = Path("bot/exts")
        for extension in path.glob("**/*.py"):
            extension = str(extension).replace("/", ".")[:-3]
            self.load_extensions(extension, store=False)
