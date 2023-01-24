import sqlite3
import time
import threading


class Users:  # main tbl with persons with their income&&outcome
    """קלאס של טבלה IncomeOutcome"""
    def __init__(self, tablename="Users", Name='Name', UserId="UserId", Email="Email",
                 Password="Password", SpotUrl="SpotUrl", SpotToken="token",Code = "Code"):
        self.tablename = tablename
        self.UserId = UserId
        self.Name = Name
        self.Email = Email
        self.Password = Password
        self.SpotUrl = SpotUrl
        self.SpotToken = SpotToken
        self.Code = Code
        conn = sqlite3.connect('MoodMusic.db')
        print("u open database successfully")
        """יוצרים טבלה אם אין"""
        CreateIfNotExist = f"create table if not exists {self.tablename} ({self.UserId} integer primary key autoincrement , " \
                           f"{self.Name} text, {self.Email} text not null , {self.Password} text not null , " \
                           f"{self.SpotUrl} text , {self.SpotToken} text, {self.Code} Code)"
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
                     f"Name: {row[1,]},\n" \
                    f"Email: {row[2]},\n" \
                    f"password: {row[3]},\n" \
                    f"SpotUrl: {row[4]},\n" \
                    f"SpotToken: {row[5]},\n"
        return query

    def insert_user(self, Name, Email, Password, SpotUrl='', SpotToken=''):
        """מכניס בן אדם לטבלה"""
        # try:
        if not self.is_exist(Email):
            conn = sqlite3.connect('MoodMusic.db')
            print("u open database successfully")
            command = f"INSERT INTO {self.tablename}({self.Name},{self.Email},{self.Password},{self.SpotUrl}," \
                    f"{self.SpotToken})" \
                    f" VALUES('{Name}','{Email}','{Password}','{SpotUrl}','{SpotToken}')"
            conn.execute(command)
            conn.commit()
            conn.close()
            print("Add User successfully")
            return True
        else:
            print("User exist so insert failed")
            return False
        # except:
        #     print("Failed to insert user")
        #     return False

    def delete_user(self, Email):
        try:
            conn = sqlite3.connect('MoodMusic.db')
            print("Opened database successfully")
            query = f"DELETE FROM Users WHERE {self.Email} = '{Email}'"
            conn.execute(query)
            conn.commit()
            conn.close()
            print("Delete User successfully")
            return True
        except:
            print("Failed to delete user")
            return False

    def is_exist(self, Email):
        try:
            conn = sqlite3.connect('MoodMusic.db')
            print("Opened database successfully")
            query = f"SELECT * from {self.tablename} where {self.Email} = '{Email}'"
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

    def Login(self, Email, Password):
        try:
            conn = sqlite3.connect('MoodMusic.db')
            print("Opened database successfully")
            query = f"SELECT * from {self.tablename} where {self.Email} = '{Email}' and {self.Password} = '{Password}'"
            cursor = conn.execute(query)
            row = cursor.fetchall()
            conn.commit()
            conn.close()
            if row:
                print("Email and pass True")
                return True
            else:
                print("Email and pass False")
                return False
        except:
            return False

    def update_password(self, Email, Password):
        try:
            conn = sqlite3.connect('MoodMusic.db')
            print("Opened database successfully")
            query = f"""
                        UPDATE Users
                        SET {self.Password} = '{Password}'
                        WHERE {self.Email} = '{Email}'
                    """
            conn.execute(query)
            conn.commit()
            conn.close()
            print("Update User successfully")
            return True
        except:
            print("Failed to Update user")
            return False

    def update_spotify(self, Email, Password, SpotUrl, SpotToken):
        try:
            conn = sqlite3.connect('MoodMusic.db')
            print("Opened database successfully")
            query = f"""
                        UPDATE Users
                        SET {self.SpotUrl} = '{SpotUrl}', {self.SpotToken} = '{SpotToken}'
                        WHERE {self.Email} = '{Email}' AND {self.Password} = '{Password}'
                    """
            conn.execute(query)
            conn.commit()
            conn.close()
            print("Update User successfully")
            return True
        except:
            print("Failed to Update user")
            return False

    def update_code(self, Email, Code):
        """מכניס בן אדם לטבלה"""
        try:
            conn = sqlite3.connect('MoodMusic.db')
            print("Opened database successfully")
            query = f"""
                                                        UPDATE Users
                                                        SET {self.Code} = '{Code}'
                                                        WHERE {self.Email} = '{Email}'
                                                    """
            conn.execute(query)
            conn.commit()
            conn.close()
            print("Update code successfully")
            x = 10
            thread = threading.Thread(target=self.delete_code, args=(Email, Code))
            thread.daemon = True
            thread.start()
            return True

        except:
            print("Failed to Update code")
            return False

    def verify_code(self, Email, Code):
        try:
            conn = sqlite3.connect('MoodMusic.db')
            print("Opened database successfully")
            query = f"SELECT * from {self.tablename} where {self.Email} = '{Email}' and {self.Code} = '{Code}'"
            cursor = conn.execute(query)
            row = cursor.fetchall()
            conn.commit()
            conn.close()
            if row:
                print("Code Exist")
                return True
            else:
                print("Code Not exist")
                return False
        except:
            return False

    def delete_code(self, Email,Code):
        try:
            time.sleep(300)
            conn = sqlite3.connect('MoodMusic.db')
            print("Opened database successfully")
            cur = conn.cursor()
            query = f"""
                    UPDATE Users
                                    SET Code = NULL
                                    WHERE Email = '{Email} AND {self.Code} = '{Code}'
            """

            conn.execute(query)
            conn.commit()
            conn.close()
            print('delete')
            return True

        except:
            print('not')
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
