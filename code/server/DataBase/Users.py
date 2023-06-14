"""
    Module Name: Users

    Description: This module provides functionality for managing users and their data in the MoodMusic application.

    Dependencies:
        - sqlite3
        - threading
        - time
        - loguru

    Classes: Users

    Author: Artur Tkach (Likva32 on GitHub)
"""

import sqlite3
import threading
import time

from loguru import logger


class Users:
    """
        Users class provides methods for managing users and their data in the MoodMusic application.
    """
    def __init__(self, tablename="Users", Name='Name', UserId="UserId", Email="Email",
                 Password="Password", SpotUrl="SpotUrl", SpotToken="token", Code="Code"):
        """
                Initialize the Users class.

                Args:
                    tablename (str): Name of the table in the database. Default is "Users".
                    Name (str): Name of the column storing user names. Default is "Name".
                    UserId (str): Name of the column storing user IDs. Default is "UserId".
                    Email (str): Name of the column storing user emails. Default is "Email".
                    Password (str): Name of the column storing user passwords. Default is "Password".
                    SpotUrl (str): Name of the column storing user Spotify URLs. Default is "SpotUrl".
                    SpotToken (str): Name of the column storing user Spotify tokens. Default is "token".
                    Code (str): Name of the column storing user verification codes. Default is "Code".
        """
        self.tablename = tablename
        self.UserId = UserId
        self.Name = Name
        self.Email = Email
        self.Password = Password
        self.SpotUrl = SpotUrl
        self.SpotToken = SpotToken
        self.Code = Code
        conn = sqlite3.connect('MoodMusic.db')
        logger.info("Opened database successfully")
        """יוצרים טבלה אם אין"""
        CreateIfNotExist = f"create table if not exists {self.tablename} ({self.UserId} integer primary key autoincrement , " \
                           f"{self.Name} text, {self.Email} text not null , {self.Password} text not null , " \
                           f"{self.SpotUrl} text , {self.SpotToken} text, {self.Code} Code)"
        conn.execute(CreateIfNotExist)
        conn.commit()
        conn.close()

    def insert_user(self, Name, Email, Password, SpotUrl='', SpotToken=''):
        """
                Insert a user into the database table.

                Args:
                    Name (str): User's name.
                    Email (str): User's email.
                    Password (str): User's password.
                    SpotUrl (str, optional): User's Spotify URL. Defaults to ''.
                    SpotToken (str, optional): User's Spotify token. Defaults to ''.

                Returns:
                    bool: True if the user was inserted successfully, False otherwise.
        """
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
                logger.info("Add User successfully")
                return True
            else:
                logger.info("User exist so insert failed")
                return False
        except:
            logger.info("Failed to insert user")
            return False
        finally:
            if conn:
                conn.close()

    def is_exist(self, Email):
        """
                Check if a user with the given email exists in the database.

                Args:
                    Email (str): User's email.
                Returns:
                    bool: True if the user exists, False otherwise.
        """
        conn = None
        try:
            conn = sqlite3.connect('MoodMusic.db')
            query = f"SELECT * from {self.tablename} where {self.Email} = (?)"
            values = (Email,)
            logger.info(query)
            cursor = conn.execute(query, values)
            row = ''
            for row in cursor:
                logger.info(row[0])
            conn.commit()
            conn.close()
            if row:
                logger.info("Exist")
                return True
            else:
                logger.info("Not exist")
                return False
        except:
            return False
        finally:
            if conn:
                conn.close()

    def Login(self, Email, Password):
        """
                Authenticate a user by checking the email and password combination.

                Args:
                    Email (str): User's email.
                    Password (str): User's password.
                Returns:
                    bool: True if the email and password combination is valid, False otherwise.
        """
        conn = None
        try:
            conn = sqlite3.connect('MoodMusic.db')
            query = f"SELECT * from {self.tablename} where {self.Email} = (?) and {self.Password} = (?)"
            values = (Email, Password)
            cursor = conn.execute(query, values)
            row = cursor.fetchall()
            conn.commit()
            conn.close()
            if row:
                logger.info("Email and pass True")
                return True
            else:
                logger.info("Email and pass False")
                return False
        except:
            return False
        finally:
            if conn:
                conn.close()

    def update_password(self, Email, Password):
        """
                Update the password for a user with the given email.

                Args:
                    Email (str): User's email.
                    Password (str): New password.
                Returns:
                    bool: True if the password was updated successfully, False otherwise.
        """
        conn = None
        try:
            conn = sqlite3.connect('MoodMusic.db')
            query = f"""
                        UPDATE Users
                        SET {self.Password} = (?)
                        WHERE {self.Email} = (?)
                    """
            values = (Password, Email)
            conn.execute(query, values)
            conn.commit()
            conn.close()
            logger.info("Update User successfully")
            return True
        except:
            logger.info("Failed to Update user")
            return False
        finally:
            if conn:
                conn.close()

    def update_spotify(self, Email, Password, SpotUrl, SpotToken):
        """
                Update the Spotify information (URL and token) for a user with the given email.

                Args:
                    Email (str): User's email.
                    Password (str): User's password.
                    SpotUrl (str): New Spotify URL.
                    SpotToken (str): New Spotify token.
                Returns:
                    bool: True if the Spotify information was updated successfully, False otherwise.
        """
        conn = None
        try:
            conn = sqlite3.connect('MoodMusic.db')
            query = f"""
                        UPDATE Users
                        SET {self.SpotUrl} = (?), {self.SpotToken} = (?)
                        WHERE {self.Email} = (?) AND {self.Password} = (?)
                    """
            values = (SpotUrl, SpotToken, Email, Password)
            conn.execute(query, values)
            conn.commit()
            conn.close()
            logger.info("Update User successfully")
            return True
        except:
            logger.info("Failed to Update user")
            return False
        finally:
            if conn:
                conn.close()

    def update_code(self, Email, Code):
        """
            Update the verification code for a user with the given email.

            Args:
                Email (str): User's email.
                Code (str): New verification code.

            Returns:
                bool: True if the code was updated successfully, False otherwise.
        """
        conn = None
        try:
            conn = sqlite3.connect('MoodMusic.db')
            query = f"""
                                                        UPDATE Users
                                                        SET {self.Code} = (?)
                                                        WHERE {self.Email} = (?)
                                                    """
            values = (Code, Email)
            conn.execute(query, values)
            conn.commit()
            conn.close()
            logger.info("Update code successfully")
            thread = threading.Thread(target=self.delete_code, args=(Email, Code))
            thread.daemon = True
            thread.start()
            return True

        except:
            logger.info("Failed to Update code")
            return False
        finally:
            if conn:
                conn.close()

    def verify_code(self, Email, Code):
        """
            Verify if the given code matches the code associated with the user's email.

            Args:
                Email (str): User's email.
                Code (str): Verification code.
            Returns:
                bool: True if the code is valid for the given email, False otherwise.
        """
        conn = None
        try:
            conn = sqlite3.connect('MoodMusic.db')
            query = f"SELECT * from {self.tablename} where {self.Email} = (?) and {self.Code} = (?)"
            values = (Email, Code)
            cursor = conn.execute(query, values)
            row = cursor.fetchall()
            conn.commit()
            conn.close()
            if row:
                logger.info("Code Exist")
                return True
            else:
                logger.info("Code Not exist")
                return False
        except:
            return False
        finally:
            if conn:
                conn.close()

    def delete_code(self, Email, Code):
        """
            Delete the verification code after a certain time period.

            Args:
                Email (str): User's email.
                Code (str): Verification code.
            Returns:
                bool: True if the code was deleted successfully, False otherwise.
        """
        conn = None
        try:
            time.sleep(300)
            conn = sqlite3.connect('MoodMusic.db')
            query = f"""
                    UPDATE Users
                                    SET Code = NULL
                                    WHERE Email = (?) AND {self.Code} = (?)
            """
            values = (Email, Code)
            conn.execute(query, values)
            conn.commit()
            conn.close()
            logger.success('delete code')
            return True
        except:
            logger.error('not delete code')
            return False
        finally:
            if conn:
                conn.close()

    def name_by_email(self, Email):
        """
            Retrieve the user's name based on their email.

            Args:
                Email (str): User's email.
            Returns:
                str: User's name if found, empty string otherwise.
        """
        name = ''
        conn = None
        try:
            conn = sqlite3.connect('MoodMusic.db')
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
        """
            Check if a Spotify URL exists for the given email.

            Args:
                Email (str): User's email.
            Returns:
                str: '1' if the URL exists, '0' otherwise.
        """
        conn = None
        try:
            conn = sqlite3.connect('MoodMusic.db')
            query = f"SELECT * from {self.tablename} where {self.Email} = '{Email}'"
            cursor = conn.execute(query)
            row = ''
            for row in cursor:
                logger.info(row[4])
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
        """
            Check if a Spotify URL exists and handle the corresponding actions.

            Args:
                Email (str): User's email.
                SpotUrl (str): Spotify URL.
                TokenInfo (str): Token information.
            Returns:
                tuple: A tuple containing the status ('Login Success', 'Login not Success') and description.
        """
        conn = None
        try:
            conn = sqlite3.connect('MoodMusic.db')
            query = f"SELECT * from {self.tablename} where {self.SpotUrl} = '{SpotUrl}'"
            cursor = conn.execute(query)
            row = ''
            for row in cursor:
                logger.info(row[2])
            conn.commit()
            conn.close()
            if row:
                if row[2] == Email:
                    logger.success('url == Email so insert token')
                    self.insert_spot_Info(Email, SpotUrl, TokenInfo)
                    status = 'Login Success'
                    description = 'you can return to Mood Music'

                else:
                    status = 'Login not Success'
                    description = 'This Spotify account already linked to another account'
                    logger.info("Url != Email so dont insert token")
            else:
                status = 'Login Successes'
                description = 'you can return to Mood Music'
                logger.info("Url Not exist - so insert url")
                self.insert_spot_Info(Email, SpotUrl, TokenInfo)
        except:
            status = 'Login not Success'
            description = 'ERROR'
            logger.error("error")
        finally:
            if conn:
                conn.close()

        return status, description

    def insert_spot_Info(self, Email, SpotUrl, TokenInfo):
        """
            Insert Spotify URL and token information for a user.

            Args:
                Email (str): User's email.
                SpotUrl (str): Spotify URL.
                TokenInfo (str): Token information.
            Returns:
                bool: True if the insertion was successful, False otherwise.
        """
        conn = None
        try:
            time.sleep(2)
            if self.is_exist(Email):
                conn = sqlite3.connect('MoodMusic.db')
                query = f"""
                                UPDATE Users
                                SET {self.SpotUrl} = (?) , {self.SpotToken} = (?)
                                WHERE {self.Email} = (?)
                         """
                values = (SpotUrl, TokenInfo, Email)
                conn.execute(query, values)
                conn.commit()
                conn.close()
                logger.success("insert SpotUrl successfully")
                return True
            else:
                logger.info("User Not Exist")
                return False
        except:
            logger.error("Failed to insert SpotUrl")
            return False
        finally:
            if conn:
                conn.close()

    def get_token(self, Email):
        """
            Retrieve the Spotify token for the given email.

            Args:
                Email (str): User's email.
            Returns:
                str: Spotify token.
        """
        conn = sqlite3.connect('MoodMusic.db')
        try:
            f = f"select {self.SpotToken} from {self.tablename} WHERE {self.Email} == (?)"
            cursor = conn.execute(f, (Email,))
            token = ''
            for row in cursor:
                token = row[0]
            return token
        finally:
            if conn:
                conn.close()
