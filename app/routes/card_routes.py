from flask import Blueprint, request
from app.models.card import Card
from ..db import db
from .route_utilities import validate_model

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")


@cards_bp.put("/<card_id>/like")
def like_card(card_id):
    card = validate_model(Card, card_id)
    card.likes_count += 1
    db.session.commit()
    return {"card": card.to_dict()}, 200


@cards_bp.delete("/<card_id>")
def delete_card(card_id):
    card = validate_model(Card, card_id)
    db.session.delete(card)
    db.session.commit()
    return {"message": "Card deleted successfully"}, 200
