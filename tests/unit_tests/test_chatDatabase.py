import pytest
import mongomock
from clueless.chat_system.chatDatabase import chatDatabase


# Create a mock database for testing
@pytest.fixture
def testdb():
    testClient = mongomock.MongoClient()
    testdb = chatDatabase(client=testClient)

    # Populate database with test messages
    game_ID = 5267
    testdb.store_chat_message(game_ID=game_ID, player_ID=1, player_Name="Tom", message="test message 1")
    testdb.store_chat_message(game_ID=game_ID, player_ID=1, player_Name="Tom", message="test message 2")
    testdb.store_chat_message(game_ID=game_ID, player_ID=2, player_Name="Jack", message="test message 3")

    return testdb


def test_get_all_chat_messages(testdb):
    game_ID = 5267
    result = list(testdb.get_all_chat_messages(game_ID))

    assert len(result) == 3


def test_store_chat_message(testdb):
    # Test parameters
    game_ID = 5267
    player_ID = 1
    player_Name = "Tom"
    message = "test message"

    testdb.store_chat_message(game_ID=game_ID, player_ID=player_ID, player_Name=player_Name, message=message)

    # Retrieve specific stored message for test check
    result = testdb.chat_messages.find_one({"game_ID": game_ID, "message_ID": 4})

    assert list(result.keys()) == [
        "game_ID",
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
    game_ID = 5267
    msg_ID = 3

    result = testdb.get_specific_message(game_ID=game_ID, msg_ID=msg_ID)
    print(result)

    assert result["message"] == "test message 3"


def test_get_specific_message_invalid(testdb):
    # Test parameters
    game_ID = 5267
    msg_ID = 10

    result = testdb.get_specific_message(game_ID=game_ID, msg_ID=msg_ID)

    assert result == "Message associated with game ID and msg ID is not found in database."
