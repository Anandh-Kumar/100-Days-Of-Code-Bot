# Copyright (c) 2022 AnandhKumar E S
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from email import message
from threading import currentThread
from bson.objectid import ObjectId
import time
import pymongo
import os
from dotenv import load_dotenv
import motor.motor_asyncio
import asyncio


class Database:
    def __init__(self, MONGO_TOKEN) -> None:
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_TOKEN)

        self.hundred_days_of_code_database = self.client["hundred_days_of_code"]
        self.guild_logs_document_collection = self.hundred_days_of_code_database[
            "server"
        ]
        self.hundred_days_of_code_user_collection = self.hundred_days_of_code_database[
            "user"
        ]
        self._user_data_format = {
            "user_id": None,
            "commits": [],
            "current_day_streak": 1,
            "highest_day_streak": 1,
            "day_until_last_commit": 0,
        }
        self._commit_format = {
            "message": None,
            "current_day_streak": 0,
            "current_higest_streak": 0,
            "message_id": None,
            "date": None,
        }
        self._guild_document = {
            "_id": None,
            "guild_id": None,
            "100DaysOfCode": None,
            "bot_updates": None,
        }

    async def add_guild(self, guild_id: int, log: str = None, value: int = None):

        guild_logs_document = await self.guild_logs_document_collection.find_one(
            {"guild_id": {"$eq": guild_id}}, {"guild_id": 1}
        )

        if not guild_logs_document:
            new_logs_document = self._guild_document
            new_logs_document["_id"] = ObjectId()
            new_logs_document["guild_id"] = guild_id

            if log and value:
                new_logs_document[log] = value

            await self.guild_logs_document_collection.insert_one(new_logs_document)

    async def set_channel(self, guild_id: int, log: str, value: int):
        """Sets a channel ID of a log in document of the guild.

        Parameters
        -----------
        guild_id: :class: 'int'
            The guild ID of the guild.
        log: :class: 'str'
            The log that need to be changed.
        value: :class: 'str'
            The value that need to be assigned to the log.
        """

        current_settings = await self.guild_logs_document_collection.find_one(
            {"guild_id": {"$eq": guild_id}}, {log: 1}
        )
        if not current_settings:
            await self.add_guild(guild_id, log, value)
            return None

        if log:
            new_settings = {"$set": {log: value}}
            await self.guild_logs_document_collection.update_one(
                current_settings, new_settings
            )
            return current_settings[log]
