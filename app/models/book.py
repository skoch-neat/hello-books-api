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

    def to_dict(self, fields=None):
        if not fields:
            book_dict = {
                'id': self.id,
                'title': self.title,
                'description': self.description
            }
        
            if self.author:
                book_dict['author'] = self.author.name

            return book_dict
            
        return {field: getattr(self, field) for field in fields if hasattr(self, field)}
    
    @classmethod
    def from_dict(cls, book_data):
        new_book = cls(
            title=book_data['title'],
            description=book_data['description']
        )

        return new_book