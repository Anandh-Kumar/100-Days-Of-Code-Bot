# Copyright (c) 2022 AnandhKumar E S
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from dotenv import load_dotenv
import discord
import os

from bot.bot import Bot


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DEBUGGING = os.getenv("DEBUGGING")

if DEBUGGING:
    command_prefix = ";"
else:
    command_prefix = "a."

intents = discord.Intents.all()

bot = Bot(command_prefix=command_prefix, intents=intents)
bot.run(BOT_TOKEN)
