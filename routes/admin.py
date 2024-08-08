from flask import Blueprint, g, escape, session, redirect, render_template, request, jsonify, Response
from app import DAO
from Misc.functions import *
from datetime import datetime

from Controllers.AdminManager import AdminManager
from Controllers.BookManager import BookManager
from Controllers.UserManager import UserManager

admin_view = Blueprint('admin_routes', __name__,
                       template_folder='../templates/admin/', url_prefix='/admin')

book_manager = BookManager(DAO)
user_manager = UserManager(DAO)
admin_manager = AdminManager(DAO)


@admin_view.route('/', methods=['GET'])
@admin_manager.admin.login_required
def home():
    admin_manager.admin.set_session(session, g)

    return render_template('admin/home.html', g=g)


@admin_view.route('/signin/', methods=['GET', 'POST'])
@admin_manager.admin.redirect_if_login
def signin():
    g.bg = 1

    if request.method == 'POST':
        _form = request.form
        email = str(_form["email"])
        password = str(_form["password"])

        if len(email) < 1 or len(password) < 1:
            return render_template('admin/signin.html', error="Email and password are required")

        d = admin_manager.signin(email, hash(password))

        if d and len(d) > 0:
            session['admin'] = int(d["id"])

            return redirect("/admin")

        return render_template('admin/signin.html', error="Email or password incorrect")

    return render_template('admin/signin.html')


@admin_view.route('/signout/', methods=['GET'])
@admin_manager.admin.login_required
def signout():
    admin_manager.signout()

    return redirect("/admin/", code=302)


@admin_view.route('/books/', methods=['GET'])
@admin_manager.admin.login_required
def books():
    admin_manager.admin.set_session(session, g)

    id = int(admin_manager.admin.uid())
    admin = admin_manager.get(id)
    mybooks = book_manager.list(availability=0)
    print(mybooks)
    return render_template('books/views.html', g=g, books=mybooks, admin=admin)


@admin_view.route('/books/<int:id>')
@admin_manager.admin.login_required
def view_book(id):
    admin_manager.admin.set_session(session, g)

    if id != None:
        b = book_manager.getBook(id)
        users = user_manager.getUsersByBook(id)

        print('----------------------------')
        print(users)

        if b and len(b) < 1:
            return render_template('books/book_view.html', error="No book found!")

        return render_template("books/book_view.html", books=b, books_owners=users, g=g)


@admin_view.route('/books/add', methods=['GET', 'POST'])
@admin_manager.admin.login_required
def book_add():
    admin_manager.admin.set_session(session, g)

    return render_template('books/add.html', g=g)


@admin_view.route('/books/edit/<int:id>', methods=['GET', 'POST'])
@admin_manager.admin.login_required
def book_edit(id):
    admin_manager.admin.set_session(session, g)

    if id != None:
        b = book_manager.getBook(id)

        if b and len(b) < 1:
            return render_template('edit.html', error="No book found!")

        return render_template("books/edit.html", book=b, g=g)

    return redirect('/books')


@admin_view.route('/books/delete/<int:id>', methods=['GET'])
@admin_manager.admin.login_required
def book_delete(id):
    id = int(id)

    if id is not None:
        book_manager.delete(id)

    return redirect('/admin/books/')


@admin_view.route('/books/search', methods=['GET'])
def search():
    admin_manager.admin.set_session(session, g)

    if "keyword" not in request.args:
        return render_template("books/view.html")

    keyword = request.args["keyword"]

    if len(keyword) < 1:
        return redirect('/admin/books')

    id = int(admin_manager.admin.uid())
    admin = admin_manager.get(id)

    d = user_manager.search(keyword, 0)

    if len(d) > 0:
        return render_template("books/views.html", search=True, books=d, count=len(d), keyword=escape(keyword), g=g, admin=admin)

    return render_template('books/views.html', error="No books found!", keyword=escape(keyword))


@admin_view.route('/users/delete/<int:id>', methods=['GET', 'POST'])
@admin_manager.admin.login_required
def users_delete(id):
    id = int(id)

    if id is not None:
        user_manager.delete(id)

    admin = admin_manager.get(id)
    myusers = admin_manager.getUsersList()
    return render_template('users.html', g=g, admin=admin, users=myusers)


@admin_view.route('/users/unlock/<int:id>', methods=['GET', 'POST'])
@admin_manager.admin.login_required
def users_unlock(id):
    admin_manager.admin.set_session(session, g)

    id = int(id)
    if id is not None:
        user_manager.unlock(id)

    adminid = int(admin_manager.admin.uid())
    admin = admin_manager.get(adminid)
    myusers = admin_manager.getUsersList()
    return render_template('users.html', g=g, admin=admin, users=myusers)


@admin_view.route('/users/lock/<int:id>', methods=['GET', 'POST'])
@admin_manager.admin.login_required
def users_lock(id):
    admin_manager.admin.set_session(session, g)
    id = int(id)

    if id is not None:
        user_manager.lock(id)

    adminid = int(admin_manager.admin.uid())
    admin = admin_manager.get(adminid)
    myusers = admin_manager.getUsersList()
    return render_template('users.html', g=g, admin=admin, users=myusers)


@admin_view.route('/users/view/', methods=['GET'])
@admin_manager.admin.login_required
def users_view():
    admin_manager.admin.set_session(session, g)

    id = int(admin_manager.admin.uid())
    admin = admin_manager.get(id)
    myusers = admin_manager.getUsersList()

    return render_template('users.html', g=g, admin=admin, users=myusers)


@admin_view.route('/users/search', methods=['GET'])
@admin_manager.admin.login_required
def user_search():
    admin_manager.admin.set_session(session, g)
    id = int(admin_manager.admin.uid())
    admin = admin_manager.get(id)

    islocked = "islocked" in request.args

    if "keyword" not in request.args:
        myusers = admin_manager.getUsersList()
        return render_template('users.html', g=g, admin=admin, users=myusers, islocked=islocked)
    print(request.form)
    keyword = request.args["keyword"]
    print("islocked : ", islocked)
    if len(keyword) < 1:
        myusers = admin_manager.getUsersList()
        return render_template('users.html', g=g, admin=admin, users=myusers, islocked=islocked)

    d = user_manager.search(keyword, 0)
    if len(d) > 0:
        return render_template("users.html", search=True, users=d, count=len(d), keyword=escape(keyword), islocked=islocked, g=g, admin=admin)

    return render_template('users.html', error="No books found!", keyword=escape(keyword), islocked=islocked)


@admin_view.route('/books/issuebook_list', methods=['GET'])
@admin_manager.admin.login_required
def issuebooks_list():
    admin_manager.admin.set_session(session, g)

    id = int(admin_manager.admin.uid())
    admin = admin_manager.get(id)
    mybooks = book_manager.list_all_book_to_issue(-1)

    return render_template('books/issuebook.html', g=g, books=mybooks, admin=admin)


@admin_view.route('/books/issuebook/<int:id>', methods=['GET'])
@admin_manager.admin.login_required
def issuebook(id):

    id = int(id)
    if id is not None:
        book_manager.issuebook(id)

    admin_manager.admin.set_session(session, g)

    adminid = int(admin_manager.admin.uid())
    admin = admin_manager.get(adminid)
    mybooks = book_manager.list_all_book_to_issue(-1)
    return render_template('books/issuebook.html', g=g, books=mybooks, admin=admin)


@admin_view.route('/books/receivebook_list', methods=['GET'])
@admin_manager.admin.login_required
def receivebooks_list():
    admin_manager.admin.set_session(session, g)

    id = int(admin_manager.admin.uid())
    admin = admin_manager.get(id)
    mybooks = book_manager.list_all_book_to_return(-1)
    print(mybooks)
    return render_template('books/receivebook.html', g=g, books=mybooks, admin=admin)


@admin_view.route('/books/receivebook/<int:id>', methods=['GET'])
@admin_manager.admin.login_required
def receivebook(id):

    id = int(id)
    if id is not None:
        book_manager.receivebook(id)

    admin_manager.admin.set_session(session, g)

    adminid = int(admin_manager.admin.uid())
    admin = admin_manager.get(adminid)
    mybooks = book_manager.list_all_book_to_return(-1)
    return redirect('../../books/receivebook_list')


@admin_view.route('/books/osbooks', methods=['GET'])
@admin_manager.admin.login_required
def osbooks_list():
    admin_manager.admin.set_session(session, g)
    rep_date = datetime.today().strftime('%d-%m-%Y')
    id = int(admin_manager.admin.uid())
    admin = admin_manager.get(id)
    mybooks = book_manager.list_all_os_book(-1)
    print(mybooks)
    return render_template('books/book_report.html', g=g, books=mybooks, repdate=rep_date, admin=admin)


@admin_view.route('/books/bookstock', methods=['GET'])
@admin_manager.admin.login_required
def bookstock_list():
    admin_manager.admin.set_session(session, g)
    rep_date = datetime.today().strftime('%d-%m-%Y')
    id = int(admin_manager.admin.uid())
    admin = admin_manager.get(id)
    mybooks = book_manager.book_stock(-1)
    print(mybooks)
    return render_template('books/book_stock.html', g=g, books=mybooks, repdate=rep_date, admin=admin)


@admin_view.route('/books/book_duereminder', methods=['GET'])
@admin_manager.admin.login_required
def book_duereminder_list():
    admin_manager.admin.set_session(session, g)
    rep_date = datetime.today().strftime('%d-%m-%Y')

    duedate = datetime.today().strftime('%d-%m-%Y')
    id = int(admin_manager.admin.uid())
    admin = admin_manager.get(id)
    mybooks = book_manager.book_duereminder_list(-1)
    print(mybooks)
    return render_template('books/book_duereminder.html', g=g, books=mybooks, repdate=rep_date, duedate=duedate, admin=admin)


@admin_view.route('/books/book_overduereminder', methods=['GET'])
@admin_manager.admin.login_required
def book_overduereminder_list():
    admin_manager.admin.set_session(session, g)
    rep_date = datetime.today().strftime('%d-%m-%Y')

    duedate = datetime.today().strftime('%d-%m-%Y')
    id = int(admin_manager.admin.uid())
    admin = admin_manager.get(id)
    mybooks = book_manager.book_overduereminder_list(-1)
    print(mybooks)
    return render_template('books/book_overduereminder.html', g=g, books=mybooks, repdate=rep_date, duedate=duedate, admin=admin)
