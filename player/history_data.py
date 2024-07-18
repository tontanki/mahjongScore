import sqlite3

from datetime import datetime


class HistoryData:
    def __init__(self, db_file='history.db'):
        self.db_file = db_file
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                player_name TEXT,
                timestamp TEXT,
                score INTEGER,
                total_score INTEGER,
                PRIMARY KEY (player_name, timestamp)
            )
        ''')
        self.connection.commit()
