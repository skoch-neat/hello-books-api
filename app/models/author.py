from sqlalchemy.orm import Mapped, mapped_column
from app.db import db

class Author (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]

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