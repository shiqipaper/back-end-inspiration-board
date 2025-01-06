from app.models.card import Card
from app.models.board import Board
import pytest


def test_to_dict_no_missing_data():
    board = Board(board_id=1, title="Inspiration", owner="Ada Lovelace")
    test_data = Card(
        card_id=1, message="Message of inspiration", likes_count=2, board_id=1
    )

    result = test_data.to_dict()

    assert len(result) == 4
    assert result["card_id"] == 1
    assert result["message"] == "Message of inspiration"
    assert result["likes_count"] == 2
    assert result["board_id"] == 1


def test_to_dict_missing_id():
    test_data = Card(message="Message of inspiration", likes_count=2, board_id=1)

    result = test_data.to_dict()

    assert len(result) == 4
    assert result["card_id"] is None
    assert result["message"] == "Message of inspiration"
    assert result["likes_count"] == 2
    assert result["board_id"] == 1


def test_to_dict_missing_message():
    test_data = Card(card_id=1, likes_count=2, board_id=1)

    result = test_data.to_dict()

    assert len(result) == 4
    assert result["card_id"] == 1
    assert result["message"] is None
    assert result["likes_count"] == 2
    assert result["board_id"] == 1


def test_to_dict_missing_likes_count():
    test_data = Card(card_id=1, message="Message of inspiration", board_id=1)

    result = test_data.to_dict()

    assert len(result) == 4
    assert result["card_id"] == 1
    assert result["message"] == "Message of inspiration"
    assert result["likes_count"] == 0
    assert result["board_id"] == 1


def test_to_dict_missing_board_id():
    board = Board(board_id=1, title="Inspiration", owner="Ada Lovelace")
    test_data = Card(
        card_id=1,
        message="Message of inspiration",
        likes_count=2,
    )

    result = test_data.to_dict()

    assert len(result) == 4
    assert result["card_id"] == 1
    assert result["message"] == "Message of inspiration"
    assert result["likes_count"] == 2
    assert result["board_id"] is None


def test_from_dict_required_properties_only_returns_card():
    card_data = {"message": "Message of inspiration", "likes_count": 2, "board_id": 1}

    new_card = Card.from_dict(card_data)

    assert new_card.message == "Message of inspiration"
    assert new_card.likes_count == 2
    assert new_card.board_id == 1


def test_from_dict_with_no_message():
    card_data = {"likes_count": 2, "board_id": 1}

    with pytest.raises(KeyError, match="message"):
        new_card = Card.from_dict(card_data)


def test_from_dict_with_no_likes_count():
    card_data = {"message": "Message of inspiration", "board_id": 1}

    new_card = Card.from_dict(card_data)

    assert new_card.message == "Message of inspiration"
    assert new_card.likes_count == 0
    assert new_card.board_id == 1


def test_from_dict_with_no_board_id():
    card_data = {"message": "Message of inspiration", "likes_count": 2}

    with pytest.raises(KeyError, match="board_id"):
        new_card = Card.from_dict(card_data)


def test_from_dict_extra_keys():
    card_data = {
        "extra": "extra stuff",
        "message": "Message of inspiration",
        "likes_count": 2,
        "board_id": 1,
    }

    new_card = Card.from_dict(card_data)

    assert new_card.message == "Message of inspiration"
    assert new_card.likes_count == 2
    assert new_card.board_id == 1
