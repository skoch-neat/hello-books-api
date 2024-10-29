from sqlalchemy.orm import Mapped, mapped_column
from app.db import db

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description
        }