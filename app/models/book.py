from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .author import Author
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import db

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("author.id"))
    author: Mapped[Optional["Author"]] = relationship(back_populates="books")

    def to_dict(self):
        book_dict = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'author': self.author.name if self.author else None
        }

        return book_dict
    
    @classmethod
    def from_dict(cls, book_data):
        return cls(
            title=book_data['title'],
            description=book_data['description'],
            author_id=book_data.get('author_id')
        )