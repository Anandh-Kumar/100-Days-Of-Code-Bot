# Copyright (c) 2022 AnandhKumar E S
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from bson.objectid import ObjectId
import time
import pymongo
import motor.motor_asyncio


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
            "current_day_streak": 0,
            "highest_day_streak": 0,
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

    async def get_guild_logs_document(self, guild_id: int, log_required=""):
        """Returns channel ID (in most cases) of a log from the guild document.

        Parameters
        -----------
        guild_id: :class: 'int'
            The guild ID of the guild.
        log: :class: 'str'
            The log that is needed from the guild logs document.
        """

        if not log_required:
            guild_logs_document = await self.guild_logs_document_collection.find_one(
                {"guild_id": {"$eq": guild_id}}
            )
        guild_logs_document = await self.guild_logs_document_collection.find_one(
            {"guild_id": {"$eq": guild_id}}, {log_required: 1}
        )
        return guild_logs_document

    async def create_user_document(
        self, user_id: int, message: str, message_id: int
    ) -> dict:
        """Add a new document to MongoDB to store user's data for hundred days of code.

        Parameters
        -----------
        user_id: :class: 'int'
            The user ID of the user.
        """

        commit = self._commit_format
        current_time = time.strftime("%a, %d %b %Y %H:%M", time.gmtime()) + " UTC"
        commit["message"] = message
        commit["message_id"] = message_id
        commit["date"] = current_time

        user_data = self._user_data_format
        user_data["_id"] = ObjectId()
        user_data["user_id"] = user_id
        user_data["commits"] = [commit]
        await self.hundred_days_of_code_user_collection.insert_one(user_data)
        return commit

    async def get_user_document(self, user_id: int, fields=[]) -> dict:
        """Returns a field or multiple fields from a user document.

        Parameters
        -----------
        user_id: :class: 'int'
            The user ID of the user.
        field: :class: 'list'
            Fields that is needed.
        """

        required_field = {}
        for field in fields:
            required_field[field] = 1

        user_data = await self.hundred_days_of_code_user_collection.find_one(
            {"user_id": {"$eq": user_id}}, required_field
        )
        return user_data

    async def get_user_day_until_last_commit(self, user_id: int) -> int:
        """Returns user's 'day until last commit' from a user document.

        Parameters
        -----------
        user_id: :class: 'int'
            The user ID of the user.
        """

        user_data = await self.get_user_document(user_id, ["day_until_last_commit"])

        if not user_data:
            return None
        return user_data["day_until_last_commit"]

    async def _update_user_document(self, user, field: str, value) -> None:
        """Update user.

        Parameters
        -----------
        user: 'user document'
            Current user document of the user.
        field:
            Field that need to be changed.
        value:
            Value for that field that need to be changed.
        """

        current_user_document = {"_id": user["_id"], field: user[field]}
        new_user_document = {"$set": {field: value}}
        await self.hundred_days_of_code_user_collection.update_one(
            current_user_document, new_user_document
        )

    async def reset_user_streak(self, user_id: int) -> None:
        """Reset 'user streak' in user document to 0.

        Parmeters
        ----------
        user_id: :class: 'int'
            The user ID of the user.
        """

        user_data = await self.get_user_document(user_id, ["current_day_streak"])
        await self._update_user_document(user_data, "current_day_streak", -1)

    async def add_new_commit(self, user_id: int, message: str, message_id: int) -> dict:
        """Add a new commit to user's.

        Parameters
        -----------
        user_id: :class: 'int'
            The user ID of the user.
        message: :class: 'str'
            The message for the commit.
        message_id: :class: 'int'
            The message id for the user.
        """

        user_data = await self.get_user_document(user_id)
        current_day_streak = user_data["current_day_streak"]
        current_highest_day_streak = user_data["highest_day_streak"]
        current_commits_list = user_data["commits"]
        current_time = time.strftime("%a, %d %b %Y %H:%M", time.gmtime()) + " UTC"
        new_commits_list = None
        print(current_day_streak, current_highest_day_streak)
        current_day_streak += 1
        await self._update_user_document(
            user_data, "current_day_streak", current_day_streak
        )
        # await self._update_user_document(user_data, "day_until_last_commit", 0)

        if current_day_streak > current_highest_day_streak:
            current_highest_day_streak = current_day_streak
            await self._update_user_document(
                user_data, "highest_day_streak", current_highest_day_streak
            )
        print(current_day_streak, current_highest_day_streak)
        commit = {
            "message": message,
            "current_day_streak": current_day_streak,
            "current_higest_streak": current_highest_day_streak,
            "message_id": message_id,
            "date": current_time,
        }

        new_commits_list = current_commits_list.copy()
        new_commits_list.append(commit)

        await self._update_user_document(user_data, "commits", new_commits_list)
        return commit
