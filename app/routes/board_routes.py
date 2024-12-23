from flask import Blueprint, request, Response
from app.models.board import Board
from app.models.card import Card
from ..db import db
from .route_utilities import validate_model, create_model

boards_bp = Blueprint('boards_bp', __name__, url_prefix='/boards')
# GET /boards
# POST /boards
# GET /boards/<board_id>/cards
# POST /boards/<board_id>/cards
@boards_bp.post("")
def create_board():
    request_body = request.get_json()
    return {"board": create_model(Board, request_body)}, 201
    

@boards_bp.get("")
def get_all_boards():
    query = db.select(Board)
    boards = db.session.scalars(query)

    boards_response = []
    for board in boards:
        boards_response.append(
            {
                "id": board.board_id,
                "title": board.title,
                "owner": board.owner
            }
        )
    return boards_response

@boards_bp.get("/<board_id>")
def get_single_board(board_id):
    board = validate_model(Board, board_id)

    return {"board": board.to_dict()}, 200

@boards_bp.post("/<board_id>/cards")
def create_card_with_board_id(board_id):
    board = validate_model(Board, board_id)
    request_body = request.get_json()

    new_card = Card(
            message=request_body["message"],
            likes_count=request_body.get("likes_count", 0),
            board_id=board.board_id
        )
    db.session.add(new_card)
    db.session.commit()

    return {"card": new_card.to_dict()}, 201

@boards_bp.get("/<board_id>/cards")
def get_cards_by_board(board_id):
    board = validate_model(Board, board_id)

    response = {
        "id": board.board_id,
        "title": board.title,
        "cards": [card.to_dict() for card in board.cards]
    }
    return response, 200
