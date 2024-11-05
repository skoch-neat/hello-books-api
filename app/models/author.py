from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .book import Book
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import db

class Author (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    books: Mapped[list["Book"]] = relationship(back_populates="author")

    def to_dict(self, fields=None):
        if not fields:
            return {
                'id': self.id,
                'name': self.name
            }
        
        return {field: getattr(self, field) for field in fields if hasattr(self, field)}
    
    @classmethod
    def from_dict(cls, author_data):
        return cls(
            name=author_data['name']
        )