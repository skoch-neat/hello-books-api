from flask import Blueprint, abort, make_response, request

from app.db import db
from app.models.author import Author
from app.models.book import Book
from app.routes.route_utilities import create_model, get_models_with_filters, validate_model

bp = Blueprint('authors_bp', __name__, url_prefix='/authors')

@bp.post('')
def create_author():
    request_body = request.get_json()
    return create_model(Author, request_body)

@bp.get('')
def get_all_authors():
    return get_models_with_filters(Author, request.args)

@bp.post("/<author_id>/books")
def create_book_with_author(author_id):
    author = validate_model(Author, author_id)
    
    request_body = request.get_json()
    request_body["author_id"] = author.id

    try:
        new_book = Book.from_dict(request_body)

    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))
        
    db.session.add(new_book)
    db.session.commit()

    return make_response(new_book.to_dict(), 201)

@bp.get('/<author_id>/books')
def get_books_by_author(author_id):
    author = validate_model(Author, author_id)
    response = [book.to_dict() for book in author.books]
    return response