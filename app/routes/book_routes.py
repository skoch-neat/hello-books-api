from flask import Blueprint, Response, request
from app.db import db
from app.models.book import Book
from app.routes.route_utilities import create_model, get_models_with_filters, validate_model

bp = Blueprint('books_bp', __name__, url_prefix='/books')

@bp.post('')
def create_book():
    return create_model(Book, request.get_json())

@bp.get('')
def get_all_books():
    return get_models_with_filters(Book, request.args)

@bp.get('/<book_id>')
def get_one_book(book_id):
    return validate_model(Book, book_id).to_dict()

@bp.put('/<book_id>')
def update_book(book_id):
    book = validate_model(Book, book_id)
    request_body = request.get_json()

    book.title = request_body['title']
    book.description = request_body['description']

    db.session.commit()
    
    return Response(status=204, mimetype='application/json')

@bp.delete('/<book_id>')
def delete_book(book_id):
    book = validate_model(Book, book_id)

    db.session.delete(book)
    db.session.commit()

    return Response(status=204, mimetype='application/json')