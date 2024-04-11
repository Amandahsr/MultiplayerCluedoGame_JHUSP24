"""
MongoDB Atlas allows global connectivity, scalability, deployment and management without the hassle of setting it up yourself.
Due to these reasons, it will be used for the chat system storage.
"""

from pymongo import MongoClient
from pytz import timezone
from datetime import datetime
from typing import Dict


class chatDatabase:
    """
    Database class to handle storage of in-game chat system messages.
    """

    def __init__(self):
        """
        Properties of database.
        """
        self.client = []
        self.database = None
        self.chatMessages = None
        self.game_active_status = False

    def connect_chat_database(self, client=None) -> None:
        """
        Connects server to chat database and initializes database properties.
        """
        if client is None:
            # Use default mongoDB server
            server_url = "localhost:27017"
            self.client.append(MongoClient(server_url))
        else:
            # Use user specified server
            self.client.append(client)

        # Switch on game active status
        self.database = self.client["cluelessChatDatabase"]
        self.chatMessages = self.database["chatMessages"]
        self.game_active_status = True

    def disconnect_chat_database(self) -> None:
        """
        Disconnects server from chat database.
        """
        # Disconnect clients
        for client in self.client:
            client.close()

        # Switch off game active status
        self.game_active_status = False

    def get_all_chat_messages(self):
        """
        Returns all chat messages stored in the database for a particular game.
        """
        # Query the database using game_ID
        messages = self.chatMessages.find()

        # Sort messages by earliest time to make messages more readable
        messages = messages.sort("message_time")

        return messages

    def store_chat_message(self, player_Name: str, character_Name: str, game_state_category: str, message: str) -> None:
        """
        Stores a chat system message in the database.

        Parameters
        player_Name: username/display name of player.
        character_Name: name of in-game character selected by player.
        game_state_category: Game category in which message is classified under. Available categories are "doorway movement", "secret passage movement", "suggestion", "accusation".
        message: Details of the game state change.
        """
        # Ensures timestamp follows EST
        msg_timeZone = timezone("US/Eastern")

        # Generate message ID for retrieval purposes: message ID is based on the number of messages in database
        msg_ID = self.chatMessages.count_documents({}) + 1

        # Message information that will be stored in database
        # Note that mongoDB will also add a "_id" key generated internally for them to identify uniquely.
        message_info = {
            "player_Name": player_Name,
            "character_Name": character_Name,
            "message_ID": msg_ID,
            "message_time": datetime.now(msg_timeZone),
            "game_state_category": game_state_category,
            "message": message,
        }

        # Store message information in database.
        self.chatMessages.insert_one(message_info)

    def get_specific_message(self, filter_flags: Dict):
        """
        Returns a message stored in the database based on message filter flags. 
        Valid filter flags are "player_Name", "character_Name", "message_ID", "message_time", "game_state_category" and "message".
        filter_flags parameter should be structured as {filter_flag: filter_flag_pattern_match} e.g. {"player_Name": "Bob"}.
        """
        # Check if filter_flag is valid
        valid_filter_flags = set(
            "player_Name", "character_Name", "message_ID", "message_time", "game_state_category", "message"
        )
        queried_filter_flags = filter_flags.keys()
        if not set(queried_filter_flags).issubset(valid_filter_flags):
            return f"There are filter flags in {queried_filter_flags} that are not valid."

        # Query database using filter flags match
        message = self.chatMessages.find(filter_flags)

        # If the message was found, return it
        if message:
            return message
        else:
            # Specify no messages if none found associated to filter flags
            return f"No messages related to {filter_flags} were found."
