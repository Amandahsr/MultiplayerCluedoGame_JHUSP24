import pytest
import mongomock
from pytz import timezone
from datetime import datetime
from clueless.chat_system.chatDatabase import chatDatabase


# Create a mock database for testing
@pytest.fixture
def testdb():
    # Create test database
    testdb = chatDatabase()
    testClient = mongomock.MongoClient()
    testdb.client = testClient
    testdb.database = testClient["cluelessChatDatabase"]
    testdb.chatMessages = testdb.database["chatMessages"]
    testdb.game_active_status = True

    # Populate database with test messages
    testdb.chatMessages.insert_one(
        {
            "player_ID": 1,
            "player_Name": "Tom",
            "message_ID": 1,
            "message_time": datetime.now(timezone("US/Eastern")),
            "message": "test message 1",
        }
    )
    testdb.chatMessages.insert_one(
        {
            "player_ID": 1,
            "player_Name": "Tom",
            "message_ID": 2,
            "message_time": datetime.now(timezone("US/Eastern")),
            "message": "test message 2",
        }
    )
    testdb.chatMessages.insert_one(
        {
            "player_ID": 2,
            "player_Name": "Jack",
            "message_ID": 3,
            "message_time": datetime.now(timezone("US/Eastern")),
            "message": "test message 3",
        }
    )

    return testdb


def test_connect_chat_database():
    # Initialize new database for testing
    testdb = chatDatabase()
    testClient = mongomock.MongoClient()

    testdb.connect_chat_database(client=testClient)

    assert testdb.client is testClient
    assert testdb.game_active_status is True


def test_disconnect_chat_database():
    # Connect to new database for testing
    testdb = chatDatabase()
    testClient = mongomock.MongoClient()
    testdb.client = testClient
    testdb.database = testClient["cluelessChatDatabase"]
    testdb.chatMessages = testdb.database["chatMessages"]
    testdb.game_active_status = True

    testdb.disconnect_chat_database()

    assert testdb.game_active_status is False


def test_get_all_chat_messages(testdb):
    result = list(testdb.get_all_chat_messages())

    assert len(result) == 3


def test_store_chat_message(testdb):
    # Test parameters
    player_ID = 1
    player_Name = "Tom"
    message = "test message"

    testdb.store_chat_message(player_ID=player_ID, player_Name=player_Name, message=message)

    # Retrieve specific stored message for test check
    result = testdb.chatMessages.find_one({"message_ID": 4})

    assert list(result.keys()) == [
        "player_ID",
        "player_Name",
        "message_ID",
        "message_time",
        "message",
        "_id",
    ]
    assert result["message"] == message


def test_get_specific_message(testdb):
    # Test parameters
    msg_ID = 3

    result = testdb.get_specific_message(msg_ID=msg_ID)
    print(result)

    assert result["message"] == "test message 3"


def test_get_specific_message_invalid(testdb):
    # Test parameters
    msg_ID = 10

    result = testdb.get_specific_message(msg_ID=msg_ID)

    assert result == "Message associated with msg ID is not found in database."
