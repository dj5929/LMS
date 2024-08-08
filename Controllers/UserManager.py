from App.User import User


class UserManager():
    def __init__(self, DAO):
        self.user = User(DAO.db.user)
        self.book = DAO.db.book
        self.dao = self.user.dao

    def list(self):
        user_list = self.dao.list()

        return user_list

    def signin(self, email, password):
        user = self.dao.getByEmail(email)

        if user is None:
            return False

        user_pass = user['password']  # user pass at
        if user_pass != password:
            return False

        return user

    def signout(self):
        self.user.signout()

    def get(self, id):
        user = self.dao.getById(id)

        return user

    def signup(self, name, email, password, dept, usergroup, regid):
        user = self.dao.getByEmail(email)

        if user is not None:
            return "already_exists"

        user_info = {"name": name, "email": email, "password": password,
                     "dept": dept, "usergroup": usergroup, "regid": regid}

        new_user = self.dao.add(user_info)

        return new_user

    def delete(self, id):
        new_user = self.dao.delete(id)

        return new_user

    def unlock(self, id):
        new_user = self.dao.unlock(id)

        return new_user

    def lock(self, id):
        new_user = self.dao.lock(id)

        return new_user

    def search(self, keyword, availability=1):
        users = self.dao.search_user(keyword, availability)
        print(users)
        return users

    def get(self, id):
        user = self.dao.getById(id)

        return user

    def update(self, name, email, password, bio, dept, usergroup, regid, id):
        user_info = {"name": name, "email": email, "password": password,
                     "bio": bio, "dept": dept, "usergroup": usergroup, "regid": regid}

        user = self.dao.update(user_info, id)

        return user

    def getBooksList(self, id):
        return self.book.getBooksByUser(id)

    def getReturnedBooksList(self, id):
        return self.book.getReturnedBooksByUser(id)

    def getUsersByBook(self, book_id):
        return self.dao.getUsersByBook(book_id)
