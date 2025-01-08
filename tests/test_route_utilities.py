from app.routes.route_utilities import validate_model, create_model
from werkzeug.exceptions import HTTPException
from app.models.board import Board
from app.models.card import Card
from flask import Flask
import pytest


def test_validate_model_board(two_saved_boards):
    result_board = validate_model(Board, 1)

    assert result_board.board_id == 1
    assert result_board.title == "Medical Humor"
    assert result_board.owner == "Meredith Grey"


def test_validate_model_board_missing_record(two_saved_boards):
    with pytest.raises(HTTPException) as error:
        result_board = validate_model(Board, "3")

    response = error.value.response
    assert response.status == "404 NOT FOUND"
    assert response.json == {"message": "Board 3 not found"}


def test_validate_model_board_invalid_id(two_saved_boards):
    with pytest.raises(HTTPException) as error:
        result_board = validate_model(Board, "dog")

    response = error.value.response
    assert response.status == "400 BAD REQUEST"
    assert response.json == {"message": "Board dog is invalid"}


def test_validate_model_invalid_model():
    app = Flask(__name__)

    with app.app_context():
        with pytest.raises(HTTPException) as error:
            result = validate_model(int, 3)

    response = error.value.response
    assert response.status == "500 INTERNAL SERVER ERROR"


def test_create_model_board(client):
    test_data = {"title": "Inspirational Quotes", "owner": "David Goggins"}

    result = create_model(Board, test_data)

    assert result == {
        "board_id": 1,
        "title": "Inspirational Quotes",
        "owner": "David Goggins",
    }


def test_create_model_board_missing_data(client):
    test_data = {"owner": "David Goggins"}

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
    test_data = {"message": "Quote", "board_id": 1}

    result = create_model(Card, test_data)

    assert result == {"card_id": 1, "message": "Quote", "likes_count": 0, "board_id": 1}


def test_create_model_card_missing_data(client, one_saved_board):
    test_data = {
        "board_id": 1,
    }

    with pytest.raises(HTTPException) as error:
        result_card = create_model(Card, test_data)

    response = error.value.response
    assert response.status == "400 BAD REQUEST"
