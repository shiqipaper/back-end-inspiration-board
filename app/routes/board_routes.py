from flask import Blueprint, request, Response
from app.models.board import Board
from app.models.card import Card
from ..db import db
from .route_utilities import validate_model, create_model
import os
import requests

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
    request_body["board_id"] = board.board_id
    
    if "message" not in request_body or not request_body["message"].strip():
        return {"message": "Invalid message"}, 400
    if len(request_body["message"]) > 40:
        return {"message": "Invalid message. Length is over 40 characters"}, 400
    card = create_model(Card, request_body)
    message_on_slack_channel(board.title, card["message"])
    return {"card": card}, 201

def message_on_slack_channel(board, message):    
    request_body = {
        "token": os.environ.get("SLACK_BOT_TOKEN"),
        "channel": os.environ.get("SLACK_CHANNEL_ID"), 
        "text": f"Card created on _{board}_: \"{message}\""
    }
    requests.post("https://slack.com/api/chat.postMessage", data=request_body)

@boards_bp.get("/<board_id>/cards")
def get_cards_by_board(board_id):
    board = validate_model(Board, board_id)

    response = {
        "id": board.board_id,
        "title": board.title,
        "cards": [card.to_dict() for card in board.cards]
    }
    return response, 200
