"""
MongoDB Atlas allows global connectivity, scalability, deployment and management without the hassle of setting it up yourself.
Due to these reasons, it will be used for the chat system storage.
"""

from pymongo import MongoClient, database, collection
from pytz import timezone
from datetime import datetime
from typing import Dict, List


class chatDatabase:
    """
    Database class to handle storage of in-game chat system messages.
    """

    def __init__(self):
        """
        Properties of database.
        """
        self.dbclient: MongoClient = None
        self.database: database = None
        self.chatMessages: collection = None
        self.game_active_status: bool = False
        self.game_state_categories: List[str] = [
            "doorway movement",
            "secret passage movement",
            "suggestion",
            "accusation",
        ]
        self.msg_filter_flags: List[str] = [
            "player_Name",
            "character_Name",
            "message_ID",
            "game_state_category",
        ]

    def connect_chat_database(self) -> str:
        """
        Connects server to chat database and initializes database properties.
        Returns status of database connection.
        """
        try:
            # Use default mongoDB database uri
            db_uri = "mongodb://localhost:27017"

            # Initialize attributes of new database
            self.dbclient = MongoClient(db_uri)
            self.database = self.dbclient["cluelessChatDatabase"]
            self.chatMessages = self.database["chatMessages"]
            self.game_active_status = True

            return "New chatMessages database initialized."

        except Exception as e:
            return f"chatMessages database cannot be initialized due to {e}."

    def disconnect_chat_database(self) -> str:
        """
        Disconnects server from chat database.
        Returns status of database disconnection.
        """
        # Disconnect from database client
        self.dbclient.close()

        # Switch off game active status
        self.game_active_status = False

        return "chatMessages database disconnected."

    def store_chat_message(
        self,
        player_Name: str,
        character_Name: str,
        game_state_category: str,
        message: str,
    ) -> str:
        """
        Stores a chat system message in the database.

        #Parameters
        player_Name: username/display name of player.
        character_Name: name of in-game character selected by player.
        game_state_category: Game category in which message is classified under. Available categories are listed in self.game_state_categories.
        message: Details of the game state change.

        Returns status of message storage.
        """
        if not game_state_category in self.game_state_categories:
            return f"Invalid game_state_category, unable to store message in database. Valid game_state_categories are {self.game_state_categories}."

        try:
            # EST timestamp
            msg_timeZone = timezone("US/Eastern")

            # message ID is based on the number of messages
            msg_ID = self.chatMessages.count_documents({}) + 1

            # Message information that will be stored
            # Note that mongoDB will also add a "_id" key auto generated to identify message uniquely
            message_info = {
                "player_Name": player_Name,
                "character_Name": character_Name,
                "message_ID": msg_ID,
                "message_time": datetime.now(msg_timeZone),
                "game_state_category": game_state_category,
                "message": message,
            }

            # Store message information
            self.chatMessages.insert_one(message_info)

            return "Message is stored successfully in chatMessage database."

        except Exception as e:
            return f"Unable to store message in chatMessage database due to {e}."

    def get_specific_message(self, filter_flags: Dict) -> List[Dict]:
        """
        Returns a message stored in the database based on message info matches.
        Valid filter flags are listed in self.msg_filter_flags.

        *filter_flags parameter should be structured as {filter_flag: filter_flag_pattern_match} e.g. {"player_Name": "Bob"}.
        To return all messages in database, specify filter_flag_pattern_match as {}.
        """
        # Check if filter_flag is valid
        queried_filter_flags = filter_flags.keys()
        if not set(queried_filter_flags).issubset(set(self.msg_filter_flags)):
            return f"There are filter flags in {queried_filter_flags} that are not valid."

        # Query database using filter flags match
        messages = self.chatMessages.find(filter_flags)
        messages = [msg for msg in messages]

        # If messages not empty, return it
        if messages:
            return messages
        else:
            # Specify no messages if none found associated to filter flags
            return f"No messages related to {filter_flags} were found."
