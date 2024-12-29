from app.routes.route_utilities import validate_model, create_model
from werkzeug.exceptions import HTTPException
from app.models.board import Board
from app.models.card import Card
import pytest


def test_validate_model_board(two_saved_boards):
    # Act
    result_board = validate_model(Board, 1)

    # Assert
    assert result_board.board_id == 1
    assert result_board.title == "Medical Humor"
    assert result_board.owner == "Meredith Grey"


def test_validate_model_board_missing_record(two_saved_boards):
    # Act & Assert
    # Calling `validate_model` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException) as error:
        result_board = validate_model(Board, "3")

    response = error.value.response
    assert response.status == "404 NOT FOUND"


def test_validate_model_board_invalid_id(two_saved_boards):
    # Act & Assert
    # Calling `validate_model` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException) as error:
        result_board = validate_model(Board, "dog")

    response = error.value.response
    assert response.status == "400 BAD REQUEST"


# We use the `client` fixture because we need an
# application context to work with the database session
def test_create_model_board(client):
    # Arrange
    test_data = {
        "title": "Inspirational Quotes",
        "owner": "David Goggins"
    }

    # Act
    result = create_model(Board, test_data)

    # Assert
    assert result == {
        "board_id": 1,
        "title": "Inspirational Quotes",
        "owner": "David Goggins"
    }


def test_create_model_board_missing_data(client):
    # Arrange
    test_data = {
        "owner": "David Goggins"
    }

    # Act & Assert
    # Calling `create_model` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException) as error:
        result_board = create_model(Board, test_data)

    response = error.value.response
    assert response.status == "400 BAD REQUEST"


def test_validate_model_card(board_with_two_cards):
    result_board = validate_model(Card, 1)
    assert result_board.card_id == 1
    assert result_board.board_id == 1
    assert result_board.message == "Simplicity is the soul of efficiency"
    assert result_board.likes_count == 0


def test_validate_model_card_missing_record(board_with_two_cards):
    with pytest.raises(HTTPException) as error:
        result_card = validate_model(Card, "3")
    response = error.value.response
    assert response.status == "404 NOT FOUND"


def test_validate_model_card_invalid_id(board_with_two_cards):
    with pytest.raises(HTTPException) as error:
        result_card = validate_model(Card, "dog")
    response = error.value.response
    assert response.status == "400 BAD REQUEST"


def test_create_model_card(client, one_saved_board):
    test_data = {
        "message": "Quote",
        "board_id": 1
    }

    result = create_model(Card, test_data)
    
    assert result == {
        "card_id": 1,
        "message": "Quote",
        "likes_count": 0,
        "board_id": 1
    }


def test_create_model_card_missing_data(client, one_saved_board):
    test_data = {
        "board_id": 1,
    }

    with pytest.raises(HTTPException) as error:
        result_card = create_model(Card, test_data)

    response = error.value.response
    assert response.status == "400 BAD REQUEST"
