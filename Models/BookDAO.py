from datetime import date


class BookDAO():
    def __init__(self, DAO):
        self.db = DAO
        self.db.table = "books"

    def delete(self, id):
        q = self.db.query("DELETE FROM @table where id={}".format(id))
        self.db.commit()

        return q

    def reserve(self, user_id, book_id):
        if not self.available(book_id):
            return "err_out"

        q = self.db.query(
            "INSERT INTO reserve (user_id, book_id) VALUES('{}', '{}');".format(user_id, book_id))

        self.db.query(
            "UPDATE @table set count=count-1 where id={};".format(book_id))
        self.db.commit()

        return q

    def issuebook(self, id):

        q = self.db.query(
            "UPDATE reserve set issued_date=now(), creditdays=15, returned=1 where id={}".format(id))

        self.db.commit()

        return q

    def receivebook(self, id):
        print("UPDATE reserve set returned_date=now(), delay_days=DATEDIFF(now(),issued_date) - creditdays , fine_amt = if(DATEDIFF(now(),issued_date) - creditdays <= 0,10, (DATEDIFF(now(),issued_date) - creditdays) *2)  where id={}".format(id))
        q = self.db.query(
            "UPDATE reserve set returned_date=now(), delay_days=DATEDIFF(now(),issued_date)- creditdays  , fine_amt = if(DATEDIFF(now(),issued_date) - creditdays <= 0,10, (DATEDIFF(now(),issued_date) - creditdays) *2)  where id={}".format(id))

        self.db.commit()

        return q

    def bookreturn(self, user_id, id):

        resever_books = self.db.query(
            "select book_id from reserve where id={};".format(id))
        for book in resever_books:
            book_id = book["book_id"]
        q = self.db.query(
            "update reserve set returned=2 where id={} and user_id={} and book_id={};".format(id, user_id, book_id))
        self.db.query(
            "UPDATE @table set count=count+1 where id={};".format(book_id))
        self.db.commit()

        return q

    def bookcancel(self, user_id, id):

        resever_books = self.db.query(
            "select book_id from reserve where id={};".format(id))
        for book in resever_books:
            book_id = book["book_id"]
        q = self.db.query(
            "delete from reserve where id={} and user_id={} and book_id={};".format(id, user_id, book_id))
        self.db.query(
            "UPDATE @table set count=count+1 where id={};".format(book_id))
        self.db.commit()

        return q

    def list_all_book_to_issue(self, user_id):

        if (user_id == -1):
            temp = "select books.id bookmaster_id,books.name,books.desc,books.author,books.availability,books.count,reserve.id,reserve.user_id,reserve.book_id,reserve.returned,reserve.issued_date,users.name username,users.email,users.mob from books left join reserve on reserve.book_id = books.id left join users on `users`.id = reserve.user_id where reserve.returned=0"
        else:
            temp = "select books.id bookmaster_id,books.name,books.desc,books.author,books.availability,books.count,reserve.id,reserve.user_id,reserve.book_id,reserve.returned,reserve.issued_date,users.name username,users.email,users.mob from books left join reserve on reserve.book_id = books.id left join users on `users`.id = reserve.user_id where reserve.returned=0 and reserve.user_id={}".format(
                user_id)
        print(temp)
        q = self.db.query(temp)

        books = q.fetchall()

        print(books)
        return books

    def list_all_book_to_return(self, user_id):

        if (user_id == -1):
            temp = "select books.id bookmaster_id,books.name,books.desc,books.author,books.availability,books.count,reserve.id,reserve.user_id,reserve.book_id,reserve.returned,reserve.issued_date,users.name username,users.email,users.mob from books left join reserve on reserve.book_id = books.id left join users on `users`.id = reserve.user_id where reserve.returned=2 and returned_date  IS NULL"
        else:
            temp = "select books.id bookmaster_id,books.name,books.desc,books.author,books.availability,books.count,reserve.id,reserve.user_id,reserve.book_id,reserve.returned,reserve.issued_date,users.name username,users.email,users.mob from books left join reserve on reserve.book_id = books.id left join users on `users`.id = reserve.user_id where reserve.returned=2 and returned_date IS NULL and reserve.user_id={}".format(
                user_id)
        print(temp)
        q = self.db.query(temp)

        books = q.fetchall()

        print(books)
        return books

    def list_all_os_book(self, user_id):

        if (user_id == -1):
            temp = "select books.id bookmaster_id,books.name,books.desc,books.author,books.availability,books.count,reserve.id,reserve.user_id,reserve.book_id,reserve.returned,reserve.issued_date,users.name username,users.regid,users.dept,users.email,users.mob from books left join reserve on reserve.book_id = books.id left join users on `users`.id = reserve.user_id where reserve.returned=1 "
        else:
            temp = "select books.id bookmaster_id,books.name,books.desc,books.author,books.availability,books.count,reserve.id,reserve.user_id,reserve.book_id,reserve.returned,reserve.issued_date,users.name username,users.regid,users.dept,users.email,users.mob from books left join reserve on reserve.book_id = books.id left join users on `users`.id = reserve.user_id where reserve.returned=1 and reserve.user_id={}".format(
                user_id)
        print(temp)
        q = self.db.query(temp)

        books = q.fetchall()

        print(books)
        return books

    def book_stock(self, user_id):

        if (user_id == -1):
            temp = "select id,name,`desc`,author,availability,edition,`count` from books"
        else:
            temp = "select id,name,`desc`,author,availability,edition,`count` from books"
        print(temp)
        q = self.db.query(temp)

        books = q.fetchall()

        print(books)
        return books

    def book_duereminder_list(self, user_id):

        if (user_id == -1):
            temp = "select DATE_ADD(issued_date, INTERVAL creditdays DAY) as due_date,books.id bookmaster_id,books.name,books.desc,books.author,books.availability,books.count,reserve.id,reserve.user_id,reserve.book_id,reserve.returned,reserve.issued_date,users.name username,users.regid,users.dept,users.email,users.mob from books left join reserve on reserve.book_id = books.id left join users on `users`.id = reserve.user_id where  reserve.returned_date is NULL  and DATE_ADD(issued_date, INTERVAL creditdays DAY) = DATE_ADD(CURRENT_DATE , INTERVAL 1 DAY);"
        else:
            temp = "select DATE_ADD(issued_date, INTERVAL creditdays DAY) as due_date,books.id bookmaster_id,books.name,books.desc,books.author,books.availability,books.count,reserve.id,reserve.user_id,reserve.book_id,reserve.returned,reserve.issued_date,users.name username,users.regid,users.dept,users.email,users.mob from books left join reserve on reserve.book_id = books.id left join users on `users`.id = reserve.user_id where  reserve.returned_date is NULL  and DATE_ADD(issued_date, INTERVAL creditdays DAY) = DATE_ADD(CURRENT_DATE , INTERVAL 1 DAY) and reserve.user_id={}".format(
                user_id)
        print(temp)
        q = self.db.query(temp)

        books = q.fetchall()

        print(books)
        return books

    def book_overduereminder_list(self, user_id):

        if (user_id == -1):
            temp = "select DATEDIFF(current_date,issued_date) - creditdays as delayed_days,DATE_ADD(issued_date, INTERVAL creditdays DAY) as due_date,books.id bookmaster_id,books.name,books.desc,books.author,books.availability,books.count,reserve.id,reserve.user_id,reserve.book_id,reserve.returned,reserve.issued_date,users.name username,users.regid,users.dept,users.email,users.mob from books left join reserve on reserve.book_id = books.id left join users on `users`.id = reserve.user_id where  reserve.returned_date is NULL  and DATE_ADD(issued_date, INTERVAL creditdays DAY) < CURRENT_DATE "
        else:
            temp = "select DATEDIFF(current_date,issued_date) - creditdays as delayed_days,DATE_ADD(issued_date, INTERVAL creditdays DAY) as due_date,books.id bookmaster_id,books.name,books.desc,books.author,books.availability,books.count,reserve.id,reserve.user_id,reserve.book_id,reserve.returned,reserve.issued_date,users.name username,users.regid,users.dept,users.email,users.mob from books left join reserve on reserve.book_id = books.id left join users on `users`.id = reserve.user_id where  reserve.returned_date is NULL  and DATE_ADD(issued_date, INTERVAL creditdays DAY) < CURRENT_DATE and reserve.user_id={}".format(
                user_id)
        print(temp)
        q = self.db.query(temp)

        books = q.fetchall()

        print(books)
        return books

    def getBooksByUser(self, user_id):
        q = self.db.query(
            "select books.id bookmaster_id,books.name,books.desc,books.author,books.availability,books.count,reserve.id,reserve.user_id,reserve.book_id,reserve.returned,reserve.issued_date from books left join reserve on reserve.book_id = books.id where reserve.returned<>2 and reserve.user_id={}".format(user_id))

        books = q.fetchall()

        print(books)
        return books

    def getReturnedBooksByUser(self, user_id):
        q = self.db.query(
            "select * from @table  left join reserve on reserve.book_id = @table.id where reserve.returned=2 and reserve.user_id={}".format(user_id))
        Returnedbooks = q.fetchall()
        for book in Returnedbooks:
            print(book)
            if (book["issued_date"]):
                book["issued_date"] = book["issued_date"].strftime("%d/%m/%Y")
            if (book["returned_date"]):
                book["returned_date"] = book["returned_date"].strftime(
                    "%d/%m/%Y")
        print(Returnedbooks)
        return Returnedbooks

    def getBooksCountByUser(self, user_id):
        q = self.db.query(
            "select count(reserve.book_id) as books_count from @table left join reserve on reserve.book_id = @table.id where reserve.returned=0 and reserve.user_id={}".format(user_id))

        books = q.fetchall()

        print(books)
        return books

    def getBook(self, id):
        q = self.db.query("select * from @table where id={}".format(id))

        book = q.fetchone()

        print(book)
        return book

    def addbook(self, books):
        # book_info = {"title": title, "bookid": bookid, "available": available, "subject": subject, "author": author, "publication": publication, "file": file, "desc":desc}

        title = books['title']
        bookid = books['bookid']
        available = books['available']
        subject = books['subject']
        author = books['author']
        publication = books['publication']
        file = books['file']
        remark = books['desc']
        query = "INSERT INTO books (name, remark, edition, availability, subject, author, publication) VALUES('{}', '{}', '{}','{}', '{}', '{}', '{}');".format(
            title, remark, bookid, available, subject, author, publication)
        print(query)
        q = self.db.query(query)
        self.db.commit()

        return q

    def available(self, id):
        book = self.getById(id)
        count = book['count']

        if count < 1:
            return False

        return True

    def getById(self, id):
        q = self.db.query("select * from @table where id='{}'".format(id))

        book = q.fetchone()

        return book

    def list(self, availability=1):
        query = "select * from @table"
        # Usually when no-admin user query for book
        if availability == 1:
            query = query+"  WHERE availability={}".format(availability)

        books = self.db.query(query)

        books = books.fetchall()

        return books

    def getReserverdBooksByUser(self, user_id):
        query = "select concat(book_id,',') as user_books from reserve WHERE user_id={}".format(
            user_id)

        books = self.db.query(query)

        books = books.fetchone()

        return books

    def search_book(self, name, availability=1):
        query = "select * from @table where name LIKE '%{}%'".format(name)

        # Usually when no-admin user query for book
        if availability == 1:
            query = query+"  AND availability={}".format(availability)

        q = self.db.query(query)
        books = q.fetchall()

        return books
