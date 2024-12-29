from app.models.board import Board
import pytest


def test_to_dict_no_missing_data():
    # Arrange
    test_data = Board(board_id=1, title="Inspiration", owner="Ada Lovelace")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 3
    assert result["board_id"] == 1
    assert result["title"] == "Inspiration"
    assert result["owner"] == "Ada Lovelace"


def test_to_dict_missing_id():
    # Arrange
    test_data = Board(title="Inspiration", owner="Ada Lovelace")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 3
    assert result["board_id"] is None
    assert result["title"] == "Inspiration"
    assert result["owner"] == "Ada Lovelace"


def test_to_dict_missing_title():
    # Arrange
    test_data = Board(board_id=1, owner="Ada Lovelace")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 3
    assert result["board_id"] == 1
    assert result["title"] is None
    assert result["owner"] == "Ada Lovelace"


def test_to_dict_missing_owner():
    # Arrange
    test_data = Board(board_id=1, title="Inspiration")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 3
    assert result["board_id"] == 1
    assert result["title"] == "Inspiration"
    assert result["owner"] is None


def test_from_dict_returns_owner():
    # Arrange
    board_data = {"title": "New Board", "owner": "New Owner"}

    # Act
    new_board = Board.from_dict(board_data)

    # Assert
    assert new_board.owner == "New Owner"


def test_from_dict_with_no_title():
    # Arrange
    board_data = {"owner": "New Owner"}

    # Act & Assert
    with pytest.raises(KeyError, match = 'title'):
        new_board = Board.from_dict(board_data)


def test_from_dict_with_no_owner():
    # Arrange
    board_data = {"title": "New Title"}

    # Act & Assert
    with pytest.raises(KeyError, match = 'owner'):
        new_board = Board.from_dict(board_data)


def test_from_dict_with_extra_keys():
    # Arrange
    board_data = {
        "extra": "some stuff",
        "title": "New Title",
        "owner": "New Owner"
    }
    
    # Act
    new_board = Board.from_dict(board_data)

    # Assert
    assert new_board.title == "New Title"
