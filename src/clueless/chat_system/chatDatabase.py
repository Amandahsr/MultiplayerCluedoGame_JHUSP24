"""
MongoDB Atlas allows global connectivity, scalability, deployment and management without the hassle of setting it up yourself.
Due to these reasons, it will be used for the chat system storage.
"""

from pymongo import MongoClient
from pytz import timezone
from datetime import datetime


class chatDatabase:
    """
    Database class to handle storage of in-game chat system messages.
    """

    def __init__(self, client=None):
        """
        Creates a new chat database to use and connect.
        """
        if client is None:
            # Use default mongoDB server
            self.server_url = "localhost:27017"
            self.client = MongoClient(self.server_url)
        else:
            self.client = client

        self.database = self.client["cluelessChatDatabase"]
        self.chat_messages = self.database["chatMessages"]

    def get_all_chat_messages(self, game_ID: int):
        """
        Returns all chat messages stored in the database for a particular game.
        """
        # Query the database using game_ID
        messages = self.chat_messages.find({"game_ID": game_ID})

        # Sort messages by earliest time to make messages more readable
        messages = messages.sort("message_time")

        return messages

    def store_chat_message(self, game_ID: int, player_ID: int, player_Name: str, message: str) -> None:
        """
        Stores a chat system message in the database.
        """
        # Ensures timestamp follows EST
        msg_timeZone = timezone("US/Eastern")

        # Generate message ID for retrieval purposes: message ID is based on the number of messages in database
        msg_ID = self.chat_messages.count_documents({"game_ID": game_ID}) + 1

        # Message information that will be stored in database
        # Note that mongoDB will also add a "_id" key generated internally for them to identify uniquely.
        message_info = {
            "game_ID": game_ID,
            "player_ID": player_ID,
            "player_Name": player_Name,
            "message_ID": msg_ID,
            "message_time": datetime.now(msg_timeZone),
            "message": message,
        }

        # Store message information in database.
        self.chat_messages.insert_one(message_info)

    def get_specific_message(self, game_ID: int, msg_ID: int):
        """
        Returns a message stored in the database based on the game_ID and msg_ID.
        """
        # Query database using game_ID and msg_ID
        message = self.chat_messages.find_one({"game_ID": game_ID, "message_ID": msg_ID})

        # If the message was found, return it
        if message:
            return message
        else:
            # Return error message stating ID is not found.
            return "Message associated with game ID and msg ID is not found in database."
