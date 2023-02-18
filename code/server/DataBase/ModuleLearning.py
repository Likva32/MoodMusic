import sqlite3


class ModuleLearning:  # main.html tbl with persons with their income&&outcome
    """קלאס של טבלה IncomeOutcome"""

    def __init__(self, tablename="ModuleLearning", PhotoId="PhotoId", Mood="Mood",
                 Photo="Photo"):
        self.tablename = tablename
        self.PhotoId = PhotoId
        self.Mood = Mood
        self.Photo = Photo
        conn = sqlite3.connect('MoodMusic.db')
        print("u open database successfully")
        """יוצרים טבלה אם אין"""
        CreateIfNotExist = f"create table if not exists {self.tablename} ({self.PhotoId} integer primary key autoincrement , " \
                           f"{self.Mood} text not null, {self.Photo} bytes)"
        conn.execute(CreateIfNotExist)
        conn.commit()
        conn.close()


ModuleLearning()
