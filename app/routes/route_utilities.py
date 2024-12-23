from flask import abort, make_response
from ..db import db
from app.models.board import Board
from app.models.card import Card

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"message": f"{cls.__name__} {model_id} is invalid"}
        abort(make_response(response , 400))

    if cls.__name__ == "Board":
        query = db.select(Board).where(Board.board_id == model_id)
    elif cls.__name__ == "Card":
        query = db.select(Card).where(Card.card_id == model_id)
    else:
        response = {"message": "Invalid model type"}
        abort(make_response(response, 500))

    model = db.session.scalar(query)
    
    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))
    
    return model


def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    
    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict()

