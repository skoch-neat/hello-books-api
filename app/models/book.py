from sqlalchemy.orm import Mapped, mapped_column
from app.db import db

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]

    def to_dict(self, fields=None):
        if not fields:
            return {
                'id': self.id,
                'title': self.title,
                'description': self.description
            }
        
        return {field: getattr(self, field) for field in fields if hasattr(self, field)}
    
    @classmethod
    def from_dict(cls, book_data):
        new_book = cls(
            title=book_data['title'],
            description=book_data['description']
        )

        return new_book