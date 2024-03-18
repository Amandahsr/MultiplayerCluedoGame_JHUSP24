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

    def __init__(self):
        """
        Properties of database.
        """
        self.client = None
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
            self.client = MongoClient(server_url)
        else:
            # Use user specified server
            self.client = client

        # Switch on game active status
        self.database = self.client["cluelessChatDatabase"]
        self.chatMessages = self.database["chatMessages"]
        self.game_active_status = True

    def disconnect_chat_database(self) -> None:
        """
        Disconnects server from chat database.
        """
        # Disconnect client
        self.client.close()

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

    def store_chat_message(self, player_ID: int, player_Name: str, character_Name: str, message: str) -> None:
        """
        Stores a chat system message in the database.
        """
        # Ensures timestamp follows EST
        msg_timeZone = timezone("US/Eastern")

        # Generate message ID for retrieval purposes: message ID is based on the number of messages in database
        msg_ID = self.chatMessages.count_documents({}) + 1

        # Message information that will be stored in database
        # Note that mongoDB will also add a "_id" key generated internally for them to identify uniquely.
        message_info = {
            "player_ID": player_ID,
            "player_Name": player_Name,
            "character_Name": character_Name,
            "message_ID": msg_ID,
            "message_time": datetime.now(msg_timeZone),
            "message": message,
        }

        # Store message information in database.
        self.chatMessages.insert_one(message_info)

    def get_specific_message(self, msg_ID: int):
        """
        Returns a message stored in the database based on the game_ID and msg_ID.
        """
        # Query database using game_ID and msg_ID
        message = self.chatMessages.find_one({"message_ID": msg_ID})

        # If the message was found, return it
        if message:
            return message
        else:
            # Return error message stating ID is not found.
            return "Message associated with msg ID is not found in database."
