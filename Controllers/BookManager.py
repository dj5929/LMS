from App.Books import Books


class BookManager():
    def __init__(self, DAO):
        self.misc = Books(DAO.db.book)
        self.dao = self.misc.dao

    def list(self, availability=1, user_id=None):
        if user_id != None:
            book_list = self.dao.listByUser(user_id)
        else:
            book_list = self.dao.list(availability)

        return book_list

    def addbook(self, title, bookid, available, subject, author, publication, file, desc):
        # book = self.dao.getBytitle(title)

        # if book is not None:
        #     return "already_exists"

        book_info = {"title": title, "bookid": bookid, "available": available, "subject": subject,
                     "author": author, "publication": publication, "file": file, "desc": desc}

        new_book = self.dao.addbook(book_info)

        return new_book

    def getReserverdBooksByUser(self, user_id):
        books = self.dao.getReserverdBooksByUser(user_id)

        return books

    def getBook(self, id):
        books = self.dao.getBook(id)

        return books

    def search(self, keyword, availability=1):
        books = self.dao.search_book(keyword, availability)

        return books

    def reserve(self, user_id, book_id):
        books = self.dao.reserve(user_id, book_id)

        return books

    def issuebook(self, id):
        books = self.dao.issuebook(id)
        return books

    def list_all_book_to_issue(self, user_id=None):
        if user_id != None:
            books = self.dao.list_all_book_to_issue(user_id)
        else:
            books = self.dao.list_all_book_to_issue(-1)
        return books

    def list_all_book_to_return(self, user_id=None):
        if user_id != None:
            books = self.dao.list_all_book_to_return(user_id)
        else:
            books = self.dao.list_all_book_to_return(-1)
        return books

    def list_all_os_book(self, user_id=None):
        if user_id != None:
            books = self.dao.list_all_os_book(user_id)
        else:
            books = self.dao.list_all_os_book(-1)
        return books

    def book_stock(self, user_id=None):
        if user_id != None:
            books = self.dao.book_stock(user_id)
        else:
            books = self.dao.book_stock(-1)
        return books

    def book_duereminder_list(self, user_id=None):
        if user_id != None:
            books = self.dao.book_duereminder_list(user_id)
        else:
            books = self.dao.book_duereminder_list(-1)
        return books

    def book_overduereminder_list(self, user_id=None):
        if user_id != None:
            books = self.dao.book_overduereminder_list(user_id)
        else:
            books = self.dao.book_overduereminder_list(-1)
        return books

    def receivebook(self, id):
        books = self.dao.receivebook(id)
        return books

    def bookreturn(self, user_id, book_id):
        books = self.dao.bookreturn(user_id, book_id)

        return books

    def bookcancel(self, user_id, book_id):
        books = self.dao.bookcancel(user_id, book_id)

        return books

    def getUserBooks(self, user_id):
        books = self.dao.getBooksByUser(user_id)

        return books

    def getReturnedBooksByUser(self, user_id):
        returnedbooks = self.dao.getReturnedBooksByUser(user_id)

        return returnedbooks

    def issuebooks(self, user_id, book_id):
        books = self.dao.reserve(user_id, book_id)

        return books

    def getUserBooksCount(self, user_id):
        books = self.dao.getBooksCountByUser(user_id)

        return books

    def delete(self, id):
        self.dao.delete(id)
