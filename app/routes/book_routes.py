from flask import Blueprint, abort, make_response, request, Response
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
    query = db.select(Book)

    title_param = request.args.get('title')
    if title_param:
        query = query.where(Book.title.ilike(f'%{title_param}%'))

    description_param = request.args.get('description')
    if description_param:
        query = query.where(Book.description.ilike(f'%{description_param}%'))

    books = db.session.scalars(query.order_by(Book.id))

    books_response = [book.to_dict() for book in books]

    return books_response

@books_bp.get('/<book_id>')
def get_one_book(book_id):
    return validate_book(book_id).to_dict()

@books_bp.put('/<book_id>')
def update_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()

    book.title = request_body['title']
    book.description = request_body['description']

    db.session.commit()
    
    return Response(status=204, mimetype='application/json')

@books_bp.delete('/<book_id>')
def delete_book(book_id):
    book = validate_book(book_id)

    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype='application/json')

def validate_book(book_id):
    try:
        book_id = int(book_id)
    except ValueError:
        abort(make_response({'message': f'book {book_id} invalid'}, 400))

    query = db.select(Book).where(Book.id == book_id)
    book = db.session.scalar(query)

    if not book:
        abort(make_response({'message': f'book {book_id} not found'}, 404))

    return book