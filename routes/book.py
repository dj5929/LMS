from flask import Blueprint, g, escape, session, redirect, render_template, request, jsonify, Response
from app import DAO

from Controllers.UserManager import UserManager
from Controllers.BookManager import BookManager

book_view = Blueprint('book_routes', __name__, template_folder='/templates')

book_manager = BookManager(DAO)
user_manager = UserManager(DAO)


@book_view.route('/books/', defaults={'id': None})
@book_view.route('/books/<int:id>')
def home(id):
    user_manager.user.set_session(session, g)

    if id != None:
        b = book_manager.getBook(id)

        print('----------------------------')
        print(b)

        user_books = {}
        if user_manager.user.isLoggedIn():
            user_books = book_manager.getReserverdBooksByUser(
                user_id=user_manager.user.uid())['user_books'].split(',')

        if b and len(b) < 1:
            return render_template('book_view.html', error="No book found!")

        return render_template("book_view.html", books=b, g=g, user_books=user_books)
    else:
        b = book_manager.list()

        user_books = []
        if user_manager.user.isLoggedIn():
            reserved_books = book_manager.getReserverdBooksByUser(
                user_id=user_manager.user.uid())

            if reserved_books is not None:
                user_books = reserved_books['user_books'].split(',')

        print("---------------------------------------")
        print(user_books)

        if b and len(b) < 1:
            return render_template('books.html', error="No books found!")

        return render_template("books.html", books=b, g=g, user_books=user_books)

    return render_template("books.html", books=b, g=g)


@book_view.route('/books/add/<id>', methods=['GET'])
@user_manager.user.login_required
def add(id):
    user_id = user_manager.user.uid()
    book_manager.reserve(user_id, id)

    b = book_manager.list()
    user_manager.user.set_session(session, g)

    return render_template("books.html", msg="Book reserved", books=b, g=g)


@book_view.route('/books/bookreturn/<id>', methods=['GET'])
@user_manager.user.login_required
def bookreturn(id):
    user_id = user_manager.user.uid()
    book_manager.bookreturn(user_id, id)
    b = book_manager.list()
    user_manager.user.set_session(session, g)
    return redirect('/user')


@book_view.route('/books/bookcancel/<id>', methods=['GET'])
@user_manager.user.login_required
def bookcancel(id):
    user_id = user_manager.user.uid()
    book_manager.bookcancel(user_id, id)
    b = book_manager.list()
    user_manager.user.set_session(session, g)
    return redirect('/user')


@book_view.route('/books/add/', methods=['GET', 'POST'])
@user_manager.user.login_required
def addbook():
    if request.method == 'POST':
        user_id = user_manager.user.uid()
        title = request.form.get('title')
        avaliable = request.form.get('avaliable')
        bookid = request.form.get('bookid')
        subject = request.form.get('subject')
        author = request.form.get('author')
        publication = request.form.get('publication')
        file = request.form.get('file')
        desc = request.form.get('desc')
        if len(title) < 1 or len(bookid) < 1 or len(subject) < 1 or len(author) < 1 or len(publication) < 1:
            return render_template('books.html', error="All fields are required")
        book_manager.addbook(
            title, bookid, avaliable, subject, author, publication, file, desc)
    return render_template("books.html", msg="Book Added")


@book_view.route('/books/search/', methods=['GET'])
def search():
    user_manager.user.set_session(session, g)

    if "keyword" not in request.args:
        return render_template("search.html")

    keyword = request.args["keyword"]

    if len(keyword) < 1:
        return redirect('/books')

    d = book_manager.search(keyword)

    if len(d) > 0:
        return render_template("books.html", search=True, books=d, count=len(d), keyword=escape(keyword), g=g)

    return render_template('books.html', error="No books found!", keyword=escape(keyword))
