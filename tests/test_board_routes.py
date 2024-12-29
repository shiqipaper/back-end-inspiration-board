def test_create_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "Code Inspo",
        "owner": "Ada"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "board": {
            "board_id": 1,
            "title": "Code Inspo",
            "owner": "Ada"
        }
    }


def test_create_board_with_no_title(client):
    # Arrange
    test_data = {
        "owner": "Ada"
    }

    # Act
    response = client.post("/boards", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {'details': 'Invalid data: missing title'}


def test_create_board_with_no_owner(client):
    # Arrange
    test_data = {
        "title": "Code Inspo"
    }

    # Act
    response = client.post("/boards", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {'details': 'Invalid data: missing owner'}


def test_create_board_with_extra_keys(client):
    # Act
    response = client.post("/boards", json={
        "extra": "some stuff",
        "title": "Code Inspo",
        "owner": "Grace Hopper"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "board": {
            "board_id": 1,
            "title": "Code Inspo",
            "owner": "Grace Hopper"
        }
    }


def test_get_all_boards_two_saved_boards(client, two_saved_boards):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0] == {
        "id": 1,
        "title": "Medical Humor",
        "owner": "Meredith Grey"
    }
    assert response_body[1] == {
        "id": 2,
        "title": "Book Quotes",
        "owner": "Alice Walker"
    }


def test_get_all_boards_one_saved_board(client, one_saved_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0] == {
        "id": 1,
        "title": "Spread Kindness",
        "owner": "Grace"
    }


def test_get_all_boards_no_saved_board(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []    


def test_get_single_board_one_saved_board(client, one_saved_board):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == {
        "board": {
            "board_id": 1,
            "title": "Spread Kindness",
            "owner": "Grace"
        }
    }


def test_get_single_board_two_saved_boards(client, two_saved_boards):
    # Act
    response = client.get("/boards/2")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == {
        "board": {
            "board_id": 2,
            "title": "Book Quotes",
            "owner": "Alice Walker"
        }
    }


def test_create_card_with_board(client, one_saved_board):
    # Arrange
    test_data = {
        "message": "Be kind"
    }

    # Act
    response = client.post("/boards/1/cards", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "card": {
            "card_id": 1,
            "message": "Be kind",
            "likes_count": 0,
            "board_id": 1
        }
    }


def test_create_card_with_nonexistant_board(client):
    # Arrange
    test_data = {
        "message": "Be kind",
    }

    # Act
    response = client.post("/boards/1/cards", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message":"Board 1 not found"}


def test_create_card_with_invalid_board_id(client):
    # Arrange
    test_data = {
        "message": "Be kind"
    }

    # Act
    response = client.post("/boards/cat/cards", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Board cat is invalid"}


def test_create_card_missing_message(client, one_saved_board):
    test_data = {}

    response = client.post("/boards/1/cards", json=test_data)
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {
        "message": "Invalid message"
    }


def test_create_card_empty_message(client, one_saved_board):
    test_data = {
        "message": ""
    }

    response = client.post("/boards/1/cards", json=test_data)
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {
        "message": "Invalid message"
    }


def test_create_card_string_of_spaces(client, one_saved_board):
    test_data = {
        "message": "     "
    }

    response = client.post("/boards/1/cards", json=test_data)
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {
        "message": "Invalid message"
    }


def test_create_card_message_exceeding_40_characters(client, one_saved_board):
    test_data = {
        "message": "Be the change you wish to see in this world"
    }

    response = client.post("/boards/1/cards", json=test_data)
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {
        "message": "Invalid message. Length is over 40 characters"
    }


def test_get_cards_by_board_expects_two_cards(client, board_with_two_cards):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body == [
        {
            "card_id": 1,
            "message": "Simplicity is the soul of efficiency",
            "likes_count": 0,
            "board_id": 1
        },
        {
            "card_id": 2,
            "message": "Hip, hip, array",
            "likes_count": 0,
            "board_id": 1
        }
    ]


def test_get_cards_by_board_with_no_cards(client, two_saved_boards):
    # Act
    response = client.get("/boards/2/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["cards"] == []


def test_get_cards_by_board_expects_two_cards(client, board_with_two_cards):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body["cards"]) == 2
