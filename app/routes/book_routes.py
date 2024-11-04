from flask import Blueprint, Response, abort, make_response, request
from app.db import db
from app.models.book import Book
from app.routes.route_utilities import validate_model

bp = Blueprint('books_bp', __name__, url_prefix='/books')

@bp.post('')
def create_book():
    request_body = request.get_json()

    try:
        new_book = Book.from_dict(request_body)
    
    except KeyError as error:
        response = {'message': f'Invalid request: missing {error.args[0]}'}
        abort(make_response(response, 400))
    
    db.session.add(new_book)
    db.session.commit()

    return new_book.to_dict(), 201

@bp.get('')
def get_all_books():
    query = db.select(Book)

    title_param = request.args.get('title')
    if title_param:
        query = query.where(Book.title.ilike(f'%{title_param}%'))

    description_param = request.args.get('description')
    if description_param:
        query = query.where(Book.description.ilike(f'%{description_param}%'))

    books = db.session.scalars(query.order_by(Book.id))

    fields_param = request.args.get('fields')
    requested_fields = fields_param.split(',') if fields_param else None

    return [book.to_dict(requested_fields) for book in books]

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