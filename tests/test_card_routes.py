def test_like_card(client, board_with_two_cards):
    response = client.put("/cards/1/like")
    response_body = response.get_json()
    assert response.status_code == 200
    assert response_body["card"]["likes_count"] == 1


def test_like_card_missing_record(client, board_with_two_cards):
    response = client.put("/cards/3/like")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message":"Card 3 not found"}


def test_like_card_invalid_id(client, board_with_two_cards):
    response = client.put("/cards/cat/like")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"message":"Card cat is invalid"}


def test_delete_card(client, board_with_two_cards):
    # Act
    response = client.delete("/cards/2")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {"message": "Card deleted successfully"}


def test_delete_card_missing_record(client, board_with_two_cards):
    response = client.delete("/cards/3")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message":"Card 3 not found"}


def test_delete_card_invalid_id(client, board_with_two_cards):
    response = client.delete("/cards/cat")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"message":"Card cat is invalid"}
