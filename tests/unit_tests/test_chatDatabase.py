import mongomock
from clueless.chatDatabase import chatDatabase
from unittest.mock import patch


# Create test database
def test_db():
    test_db = chatDatabase()
    test_db.dbclient = mongomock.MongoClient()
    test_db.database = test_db.dbclient["chatDatabase"]
    test_db.chatMessages = test_db.database["chatMessages"]
    test_db.game_active_status = True

    return test_db


def test_connect_chat_database():
    # Initialize new database for testing
    testdb = chatDatabase()
    result = testdb.connect_chat_database()

    assert result == "New chatMessages database initialized."


def test_connect_chat_database_error():
    # Mock client to raise exception for testing
    with patch("clueless.chatDatabase.MongoClient", side_effect=Exception("Failed connection")) as mock_client:
        # Initialize new database for testing
        testdb = chatDatabase()
        client_response = testdb.connect_chat_database()

        # Ensure mocked client gets called
        mock_client.assert_called_once()

        assert "chatMessages database cannot be initialized" in client_response


def test_disconnect_chat_database():
    testdb = test_db()
    client_response = testdb.disconnect_chat_database()

    assert client_response == "chatMessages database disconnected."


def test_store_chat_message():
    testdb = test_db()

    testMsg = "test message"
    db_response = testdb.store_chat_message(
        player_Name="Bob", character_Name="Peach", game_state_category="doorway movement", message=testMsg
    )

    assert testdb.chatMessages.count_documents({}) == 1
    assert "Message is stored successfully" in db_response


def test_store_chat_message_storage_error():
    testdb = test_db()

    # Patch function to raise exception for testing
    with patch("clueless.chatDatabase.timezone", side_effect=Exception("Unable to store message")) as msg_store_mock:
        testMsg = "test message"
        db_response = testdb.store_chat_message(
            player_Name="Bob", character_Name="Peach", game_state_category="doorway movement", message=testMsg
        )

        # Ensure mocked function gets called
        msg_store_mock.assert_called_once()

    assert "Unable to store message" in db_response


def test_store_chat_message_invalid_game_state_category():
    testdb = test_db()
    testMsg = "test message"
    db_response = testdb.store_chat_message(
        player_Name="Bob", character_Name="Peach", game_state_category="invalid category", message=testMsg
    )

    assert "Invalid game_state_category" in db_response


def test_get_specific_message():
    # Add one test message to testdb
    testdb = test_db()
    test_message = {
        "player_Name": "Bob",
        "character_Name": "Peach",
        "message_ID": 1,
        "message_time": "test time",
        "game_state_category": "accusation",
        "message": "test message",
    }
    testdb.chatMessages.insert_one(test_message)

    result = testdb.get_specific_message({"game_state_category": "accusation"})

    assert len(result) == 1


def test_get_specific_message_filter_flag_invalid():
    # Add one test message to testdb
    testdb = test_db()
    test_message = {
        "player_Name": "Bob",
        "character_Name": "Peach",
        "message_ID": 1,
        "message_time": "test time",
        "game_state_category": "accusation",
        "message": "test message",
    }
    testdb.chatMessages.insert_one(test_message)

    result = testdb.get_specific_message({"game_ID": 62572})

    assert "not valid" in result


def test_get_specific_message_no_matches():
    # Add one test message to testdb
    testdb = test_db()

    result = testdb.get_specific_message({"game_state_category": "accusation"})

    assert "No messages related" in result
