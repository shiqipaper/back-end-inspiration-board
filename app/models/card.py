from ..db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional


class Card(db.Model):
    card_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str]
    likes_count: Mapped[Optional[int]]
    board_id: Mapped[int] = mapped_column(ForeignKey("board.board_id"))
    board: Mapped["Board"] = relationship(back_populates="cards")

    def to_dict(self):
        card_as_dict = dict(
            card_id=self.card_id,
            message=self.message,
            likes_count=self.likes_count if self.likes_count else 0,
            board_id=self.board_id,
        )
        return card_as_dict

    @classmethod
    def from_dict(cls, card_data):
        return cls(
            message=card_data["message"],
            likes_count=card_data.get("likes_count", 0),
            board_id=card_data["board_id"],
        )
