import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from app.models.board import Board
from app.models.card import Card
from dotenv import load_dotenv
import os

load_dotenv()

@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def two_saved_boards(app):
    # Arrange
    medical_board = Board(title="Medical Humor",
                          owner="Meredith Grey")
    english_board = Board(title="Book Quotes",
                          owner="Alice Walker")

    db.session.add_all([medical_board, english_board])
    db.session.commit()


@pytest.fixture
def one_saved_board(app):
    board = Board(title="Inspirational Quotes", 
                  owner="Ada Lovelace")
    db.session.add(board)
    db.session.commit()


@pytest.fixture
def board_with_two_cards(app, one_saved_board):    
    efficiency_card = Card(message="Simplicity is the soul of efficiency",
                       likes_count=0,
                       board_id=1)
    debugging_card = Card(message="The best error message is the one that never shows up",
                       likes_count=0,
                       board_id=1)

    db.session.add_all([efficiency_card, debugging_card])
    db.session.commit()
