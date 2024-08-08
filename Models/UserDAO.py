class UserDAO():
    def __init__(self, DAO):
        self.db = DAO
        self.db.table = "users"

    def list(self):
        users = self.db.query("select @table.id,@table.name,@table.email,@table.bio,@table.mob,@table.lock,@table.created_at,count(reserve.book_id) as books_owned from @table LEFT JOIN reserve ON reserve.user_id=@table.id GROUP BY reserve.user_id").fetchall()

        return users

    def getById(self, id):
        q = self.db.query("select * from @table where id='{}'".format(id))

        user = q.fetchone()

        return user

    def getUsersByBook(self, book_id):
        q = self.db.query(
            "select * from @table LEFT JOIN reserve ON reserve.user_id = @table.id WHERE reserve.book_id={}".format(book_id))

        user = q.fetchall()

        return user

    def getByEmail(self, email):
        q = self.db.query(
            "select * from @table where email='{}'".format(email))

        user = q.fetchone()

        return user

    def delete(self, user_id):
        print("Create function to delete,unlock,lock, in userdao or admindao or bookdao  and call it from controllers  USERMANAGER ")
        temp = "delete from @table where id={}".format(user_id)
        print(temp)
        q = self.db.query("delete from @table where id={}".format(user_id))
        self.db.commit()

        return q

    def unlock(self, user_id):
        temp = "update @table set `lock`=0 where id={}".format(user_id)
        print(temp)
        q = self.db.query(
            "update @table set `lock`=0 where id={}".format(user_id))
        self.db.commit()

        return q

    def lock(self, user_id):
        temp = "update @table set lock=1 where id={}".format(user_id)
        print(temp)
        q = self.db.query(
            "update @table set `lock`=1 where id={}".format(user_id))
        self.db.commit()

        return q

    def search_user(self, name, availability=1):
        query = "select * from users where name LIKE '%{}%'".format(name)

        # Usually when no-admin user query for book
        # if availability == 1:
        #     query = query+"  AND `lock1={}".format(availability)
        print(query)
        q = self.db.query(query)
        users = q.fetchall()
        return users

    def add(self, user):
        name = user['name']
        email = user['email']
        password = user['password']
        dept = user['dept']
        usergroup = user['usergroup']
        regid = user['regid']

        q = self.db.query("INSERT INTO @table (name, email, password,dept,usergroup,regid) VALUES('{}', '{}', '{}','{}', '{}', '{}');".format(
            name, email, password, dept, usergroup, regid))
        self.db.commit()

        return q

    def update(self, user, _id):
        name = user['name']
        email = user['email']
        password = user['password']
        dept = user['dept']
        group = user['usergroup']
        regid = user['regid']
        bio = user['bio']

        q = self.db.query("UPDATE @table SET name = '{}', email='{}', password='{}', bio='{}',dept='{}',usergroup='{}',regid='{}' WHERE id={}".format(
            name, email, password, bio, dept, group, regid, _id))
        self.db.commit()

        return q
