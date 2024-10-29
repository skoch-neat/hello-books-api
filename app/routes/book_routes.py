from flask import Blueprint, abort, make_response, request
from app.db import db
from app.models.book import Book

books_bp = Blueprint('books_bp', __name__, url_prefix='/books')

@books_bp.post('')
def create_book():
    request_body = request.get_json()
    
    title = request_body['title']
    description = request_body['description']
    new_book = Book(title=title, description=description)
    
    db.session.add(new_book)
    db.session.commit()

    return new_book.to_dict(), 201

@books_bp.get('')
def get_all_books():
    query = db.select(Book).order_by(Book.id)
    books = db.session.scalars(query)

    return [book.to_dict() for book in books]

@books_bp.get('/<book_id>')
def get_one_book(book_id):
    return validate_book(book_id).to_dict()

def validate_book(book_id):
    try:
        book_id = int(book_id)
    except ValueError:
        abort(make_response({'message': f'book {book_id} invalid'}, 400))

        book = db.session.get(Book, book_id)
        if book is None:
            abort(make_response({'message': f'book {book_id} not found'}, 404))

    return book