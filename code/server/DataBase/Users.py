import sqlite3


class Users:  # main tbl with persons with their income&&outcome
    """קלאס של טבלה IncomeOutcome"""
    def __init__(self, tablename="Users", UserId="UserId", Name="Name", Username="Username",
                 Password="Password", SpotUrl="SpotUrl", SpotToken="token"):
        self.tablename = tablename
        self.UserId = UserId
        self.Name = Name
        self.Username = Username
        self.Password = Password
        self.SpotUrl = SpotUrl
        self.SpotToken = SpotToken
        conn = sqlite3.connect('MoodMusic.db')
        print("u open database successfully")
        """יוצרים טבלה אם אין"""
        CreateIfNotExist = f"create table if not exists {self.tablename} ({self.UserId} integer primary key autoincrement , " \
                           f"{self.Name} text, {self.Username} text not null , {self.Password} text not null , " \
                           f"{self.SpotUrl} text , {self.SpotToken} text)"
        conn.execute(CreateIfNotExist)
        conn.commit()
        conn.close()

    def get_all_users(self):
        """מחזיר סטרינג עם כל האנשים"""
        conn = sqlite3.connect('MoodMusic.db')
        print("Opened database successfully")
        cursor = conn.execute(f"select*from {self.tablename}")
        query = ""
        for row in cursor:
            query += f"UserId: {row[0]},\n" \
                    f"Name: {row[1]},\n" \
                    f"Username: {row[2]},\n" \
                    f"password: {row[3]},\n" \
                    f"SpotUrl: {row[4]},\n" \
                    f"SpotToken: {row[5]},\n"
        return query

    def insert_user(self, Name, Username, Password, SpotUrl='', SpotToken=''):
        """מכניס בן אדם לטבלה"""
        try:
            if not self.is_exist(Username, Password):
                conn = sqlite3.connect('MoodMusic.db')
                print("u open database successfully")
                query = f"INSERT INTO {self.tablename}({self.Name},{self.Username},{self.Password},{self.SpotUrl}," \
                        f"{self.SpotToken})" \
                        f"VALUES('{Name}','{Username}','{Password}','{SpotUrl}','{SpotToken}')"
                conn.execute(query)
                conn.commit()
                conn.close()
                print("Add User successfully")
                return True
            else:
                print("User exist so insert failed")
                return False
        except:
            print("Failed to insert user")
            return False

    def delete_user(self, Username):
        try:
            conn = sqlite3.connect('MoodMusic.db')
            print("Opened database successfully")
            query = f"DELETE FROM Users WHERE {self.Username} = '{Username}'"
            conn.execute(query)
            conn.commit()
            conn.close()
            print("Delete User successfully")
            return True
        except:
            print("Failed to delete user")
            return False

    def is_exist(self, Username, Password):
        try:
            conn = sqlite3.connect('MoodMusic.db')
            print("Opened database successfully")
            query = f"SELECT * from {self.tablename} where {self.Username} = '{Username}' and {self.Password} = '{Password}'"
            cursor = conn.execute(query)
            row = cursor.fetchall()
            conn.commit()
            conn.close()
            if row:
                print("Exist")
                return True
            else:
                print("Not exist")
                return False
        except:
            return False

    def update_password(self, Username, Password, NewPassword):
        try:
            conn = sqlite3.connect('MoodMusic.db')
            print("Opened database successfully")
            query = f"""
                        UPDATE Users
                        SET {self.Password} = '{NewPassword}'
                        WHERE {self.Username} = '{Username}' AND {self.Password} = '{Password}'
                    """
            conn.execute(query)
            conn.commit()
            conn.close()
            print("Update User successfully")
            return True
        except:
            print("Failed to Update user")
            return False

    def update_spotify(self, Username, Password, SpotUrl, SpotToken):
        try:
            conn = sqlite3.connect('MoodMusic.db')
            print("Opened database successfully")
            query = f"""
                        UPDATE Users
                        SET {self.SpotUrl} = '{SpotUrl}', {self.SpotToken} = '{SpotToken}'
                        WHERE {self.Username} = '{Username}' AND {self.Password} = '{Password}'
                    """
            conn.execute(query)
            conn.commit()
            conn.close()
            print("Update User successfully")
            return True
        except:
            print("Failed to Update user")
            return False


# U = Users()
# # U.delete_user('Dimon4ickAliant')
# U.insert_user('Artur', 'Likva', 'pass123','awd')
# # U.insert_user('Dima', 'Dimon4ickAliant', '123pass', 'https://www.spotify.com/dimon', 'tokennykcfg')
# print(U.get_all_users())
# U.is_exist('Likva32', 'pass123')
# # U.update_password('Likva32', 'pass123', 'XUIII')
# # U.update_spotify('Likva32', 'pass123', 'https://www.spotify.com/neartur', '123')
#
