"""
    Module Name: SpotifyPlaylist
    Description: This module provides a class for managing statistics related to Spotify music.

    Dependencies:
        - sqlite3: Required for working with an SQLite database.
        - loguru.logger: Required for logging messages.

    Classes:
        SpotifyStat: A class for managing Spotify statistics and interacting with an SQLite database.

    Author: Artur Tkach (Likva32 on GitHub)
"""
import sqlite3

from loguru import logger


class SpotifyStat:
    def __init__(self, tablename="SpotifyStat", Id="Id", Angry="Angry", Disgust="Disgust",
                 Fear="Fear", Happy="Happy", Sad="Sad", Surprise="Surprise", Neutral="Neutral"):
        """
                Initialize the SpotifyStat object.

                Args:
                    tablename (str, optional): The name of the table in the database. Defaults to "SpotifyStat".
                    Id (str, optional): The name of the Id column in the table. Defaults to "Id".
                    Angry (str, optional): The name of the Angry column in the table. Defaults to "Angry".
                    Disgust (str, optional): The name of the Disgust column in the table. Defaults to "Disgust".
                    Fear (str, optional): The name of the Fear column in the table. Defaults to "Fear".
                    Happy (str, optional): The name of the Happy column in the table. Defaults to "Happy".
                    Sad (str, optional): The name of the Sad column in the table. Defaults to "Sad".
                    Surprise (str, optional): The name of the Surprise column in the table. Defaults to "Surprise".
                    Neutral (str, optional): The name of the Neutral column in the table. Defaults to "Neutral".
        """
        self.tablename = tablename
        self.Id = Id
        self.Angry = Angry
        self.Disgust = Disgust
        self.Fear = Fear
        self.Happy = Happy
        self.Sad = Sad
        self.Surprise = Surprise
        self.Neutral = Neutral
        conn = sqlite3.connect('MoodMusic.db')
        logger.info("Opened database successfully")
        """יוצרים טבלה אם אין"""
        CreateIfNotExist = f"create table if not exists {self.tablename} ({self.Id} integer primary key autoincrement , " \
                           f"{self.Angry} integer not null, {self.Disgust} integer not null, {self.Fear} integer not null ," \
                           f"{self.Happy} integer not null, {self.Sad} integer not null, {self.Surprise} integer not null," \
                           f"{self.Neutral} integer not null)"
        conn.execute(CreateIfNotExist)
        conn.commit()
        conn.close()

    def insert_first_stat(self):
        """
            Insert the first stat into the table.

            Returns:
                bool: True if the stat is added successfully, False otherwise.
        """
        conn = None
        try:
            if not self.is_exist(1):
                conn = sqlite3.connect('MoodMusic.db')
                command = f"INSERT INTO {self.tablename}({self.Angry},{self.Disgust},{self.Fear},{self.Happy}," \
                          f"{self.Sad}, {self.Surprise}, {self.Neutral})" \
                          f" VALUES((?),(?),(?),(?),(?),(?),(?))"
                values = (0, 0, 0, 0, 0, 0, 0)
                conn.execute(command, values)
                conn.commit()
                conn.close()
                logger.success("Add stat successfully")
                return True
            else:
                logger.info("stat exist so insert failed")
                return False
        except:
            logger.error("Failed to Add stat")
            return False
        finally:
            if conn:
                conn.close()

    def is_exist(self, ID):
        """
            Check if a record with the given ID exists in the table.

            Args:
                ID (int): The ID to check for existence.
            Returns:
                bool: True if the record exists, False otherwise.
        """
        conn = None
        try:
            conn = sqlite3.connect('MoodMusic.db')
            query = f"SELECT * from {self.tablename} where {self.Id} = (?)"
            values = (ID,)
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

    def update_stat(self, Emote):
        """
            Update the specified Emote column in the table.

            Args:
                Emote (str): The name of the Emote column to update.
            Returns:
                bool: True if the stat is updated successfully, False otherwise.
        """
        conn = None
        try:
            base_value = self.value_by_Emote(Emote)
            conn = sqlite3.connect('MoodMusic.db')
            query = f"""
                        UPDATE {self.tablename}
                        SET {Emote} = (?)
                        WHERE {self.Id} = (?)
                    """
            values = (base_value + 1, 1)
            conn.execute(query, values)
            conn.commit()
            conn.close()
            logger.success("Update Stat successfully")
            return True
        except:
            logger.error("Failed to Update Stat")
            return False
        finally:
            if conn:
                conn.close()

    def value_by_Emote(self, Emote):
        """
            Get the value of the specified Emote column in the table.

            Args:
                Emote (str): The name of the Emote column.
            Returns:
                str: The value of the Emote column.
        """
        name = ''
        conn = None
        try:
            conn = sqlite3.connect('MoodMusic.db')
            f = f"select {Emote} from {self.tablename} WHERE {self.Id} == (?)"
            cursor = conn.execute(f, (1,))
            name = ''
            for row in cursor:
                name = row[0]
            return name
        except:
            return name
        finally:
            if conn:
                conn.close()
