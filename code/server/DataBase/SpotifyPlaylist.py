import sqlite3
import Users


class SpotifyPlaylist:  # main tbl with persons with their income&&outcome
    """קלאס של טבלה IncomeOutcome"""

    def __init__(self, tablename="SpotifyPlaylist", PlaylistId="PlaylistId", SpotUrl="SpotUrl",
                 PlaylistUrl="PlaylistUrl"):
        self.tablename = tablename
        self.PlaylistId = PlaylistId
        self.SpotUrl = SpotUrl
        self.PlaylistUrl = PlaylistUrl
        conn = sqlite3.connect('MoodMusic.db')
        print("u open database successfully")
        """יוצרים טבלה אם אין"""
        CreateIfNotExist = f"create table if not exists {self.tablename} ({self.PlaylistId} integer primary key autoincrement , " \
                           f"{self.SpotUrl} text not null, {self.PlaylistUrl} text not null)"
        conn.execute(CreateIfNotExist)
        conn.commit()
        conn.close()


SpotifyPlaylist()
m = Users.Users()
print(type(m))
