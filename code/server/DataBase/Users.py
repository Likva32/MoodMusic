import sqlite3
import threading
import time


class Users:  # main.html tbl with persons with their income&&outcome
    """קלאס של טבלה IncomeOutcome"""

    def __init__(self, tablename="Users", Name='Name', UserId="UserId", Email="Email",
                 Password="Password", SpotUrl="SpotUrl", SpotToken="token", Code="Code"):
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

    def insert_user(self, Name, Email, Password, SpotUrl='', SpotToken=''):
        """מכניס בן אדם לטבלה"""
        conn = None
        try:
            if not self.is_exist(Email):
                conn = sqlite3.connect('MoodMusic.db')
                command = f"INSERT INTO {self.tablename}({self.Name},{self.Email},{self.Password},{self.SpotUrl}," \
                          f"{self.SpotToken})" \
                          f" VALUES((?),(?),(?),(?),(?))"
                values = (Name, Email, Password, SpotUrl, SpotToken)
                conn.execute(command, values)
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
        finally:
            if conn:
                conn.close()

    # def delete_user(self, Email):
    #     try:
    #         conn = sqlite3.connect('MoodMusic.db')
    #         print("Opened database successfully")
    #         query = f"DELETE FROM Users WHERE {self.Email} = (?)"
    #         values = (Email,)
    #         conn.execute(query, values)
    #         conn.commit()
    #         conn.close()
    #         print("Delete User successfully")
    #         return True
    #     except:
    #         print("Failed to delete user")
    #         return False

    def is_exist(self, Email):
        conn = None
        try:
            conn = sqlite3.connect('MoodMusic.db')
            print("Opened database successfully")
            query = f"SELECT * from {self.tablename} where {self.Email} = (?)"
            values = (Email,)
            print(query)
            cursor = conn.execute(query, values)
            row = ''
            for row in cursor:
                print(row[0])
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
        finally:
            if conn:
                conn.close()

    def Login(self, Email, Password):
        conn = None
        try:
            conn = sqlite3.connect('MoodMusic.db')
            print("Opened database successfully")
            query = f"SELECT * from {self.tablename} where {self.Email} = (?) and {self.Password} = (?)"
            values = (Email, Password)
            cursor = conn.execute(query, values)
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
        finally:
            if conn:
                conn.close()

    def update_password(self, Email, Password):
        conn = None
        try:
            conn = sqlite3.connect('MoodMusic.db')
            print("Opened database successfully")
            query = f"""
                        UPDATE Users
                        SET {self.Password} = (?)
                        WHERE {self.Email} = (?)
                    """
            values = (Password, Email)
            conn.execute(query, values)
            conn.commit()
            conn.close()
            print("Update User successfully")
            return True
        except:
            print("Failed to Update user")
            return False
        finally:
            if conn:
                conn.close()

    def update_spotify(self, Email, Password, SpotUrl, SpotToken):
        conn = None
        try:
            conn = sqlite3.connect('MoodMusic.db')
            print("Opened database successfully")
            query = f"""
                        UPDATE Users
                        SET {self.SpotUrl} = (?), {self.SpotToken} = (?)
                        WHERE {self.Email} = (?) AND {self.Password} = (?)
                    """
            values = (SpotUrl, SpotToken, Email, Password)
            conn.execute(query, values)
            conn.commit()
            conn.close()
            print("Update User successfully")
            return True
        except:
            print("Failed to Update user")
            return False
        finally:
            if conn:
                conn.close()

    def update_code(self, Email, Code):
        """מכניס בן אדם לטבלה"""
        conn = None
        try:
            conn = sqlite3.connect('MoodMusic.db')
            print("Opened database successfully")
            query = f"""
                                                        UPDATE Users
                                                        SET {self.Code} = (?)
                                                        WHERE {self.Email} = (?)
                                                    """
            values = (Code, Email)
            conn.execute(query, values)
            conn.commit()
            conn.close()
            print("Update code successfully")
            thread = threading.Thread(target=self.delete_code, args=(Email, Code))
            thread.daemon = True
            thread.start()
            return True

        except:
            print("Failed to Update code")
            return False
        finally:
            if conn:
                conn.close()

    def verify_code(self, Email, Code):
        conn = None
        try:
            conn = sqlite3.connect('MoodMusic.db')
            print("Opened database successfully")
            query = f"SELECT * from {self.tablename} where {self.Email} = (?) and {self.Code} = (?)"
            values = (Email, Code)
            cursor = conn.execute(query, values)
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
        finally:
            if conn:
                conn.close()

    def delete_code(self, Email, Code):
        conn = None
        try:
            time.sleep(300)
            conn = sqlite3.connect('MoodMusic.db')
            print("Opened database successfully")
            cur = conn.cursor()
            query = f"""
                    UPDATE Users
                                    SET Code = NULL
                                    WHERE Email = (?) AND {self.Code} = (?)
            """
            values = (Email, Code)
            conn.execute(query)
            conn.commit()
            conn.close()
            print('delete')
            return True
        except:
            print('not')
            return False
        finally:
            if conn:
                conn.close()

    def name_by_email(self, Email):
        name = ''
        conn = None
        try:
            conn = sqlite3.connect('MoodMusic.db')
            print("Opened database successfully")
            f = f"select {self.Name} from {self.tablename} WHERE {self.Email} == (?)"
            cursor = conn.execute(f, (Email,))
            name = ''
            for row in cursor:
                name = row[0]
            return name
        except:
            return name
        finally:
            if conn:
                conn.close()

    def check_url(self, Email):
        conn = None
        try:
            conn = sqlite3.connect('MoodMusic.db')
            print("Opened database successfully")
            query = f"SELECT * from {self.tablename} where {self.Email} = '{Email}'"
            cursor = conn.execute(query)
            row = ''
            for row in cursor:
                print(row[4])
            conn.commit()
            conn.close()
            if row[4]:
                return '1'
            else:
                return '0'
        except:
            return '0'
        finally:
            if conn:
                conn.close()

    def url_exist(self, Email, SpotUrl, TokenInfo):
        status = ''
        description = ''
        conn = None
        try:
            conn = sqlite3.connect('MoodMusic.db')
            print("Opened database successfully")
            query = f"SELECT * from {self.tablename} where {self.SpotUrl} = '{SpotUrl}'"
            cursor = conn.execute(query)
            row = ''
            for row in cursor:
                print(row[2])
            conn.commit()
            conn.close()
            if row:
                if row[2] == Email:
                    print('url == Email so insert token')
                    self.insert_spot_Info(Email, SpotUrl, TokenInfo)
                    status = 'Login Success'
                    description = 'you can return to Mood Music'

                else:
                    status = 'Login not Success'
                    description = 'This Spotify account already linked to another account'
                    print("Url != Email so dont insert token")
            else:
                status = 'Login Successes'
                description = 'you can return to Mood Music'
                print("Url Not exist - so insert url")
                self.insert_spot_Info(Email, SpotUrl, TokenInfo)
        except:
            status = 'Login not Success'
            description = 'ERROR'
            print("error")
        finally:
            if conn:
                conn.close()

        return status, description

    def insert_spot_Info(self, Email, SpotUrl, TokenInfo):
        conn = None
        try:
            time.sleep(2)
            if self.is_exist(Email):
                conn = sqlite3.connect('MoodMusic.db')
                print("u open database successfully")
                query = f"""
                                UPDATE Users
                                SET {self.SpotUrl} = (?) , {self.SpotToken} = (?)
                                WHERE {self.Email} = (?)
                         """
                values = (SpotUrl, TokenInfo, Email)
                conn.execute(query, values)
                conn.commit()
                conn.close()
                print("insert SpotUrl successfully")
                return True
            else:
                print("User Not Exist")
                return False
        except:
            print("Failed to insert SpotUrl")
            return False
        finally:
            if conn:
                conn.close()

    def get_token(self, Email):
        conn = sqlite3.connect('MoodMusic.db')
        try:
            print("Opened database successfully")
            f = f"select {self.SpotToken} from {self.tablename} WHERE {self.Email} == (?)"
            cursor = conn.execute(f, (Email,))
            token = ''
            for row in cursor:
                token = row[0]
            return token
        finally:
            if conn:
                conn.close()
