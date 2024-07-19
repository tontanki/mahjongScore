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
                PRIMARY KEY (player_name, timestamp)
            )
        ''')
        self.connection.commit()

    async def insert_score(self, player_name, score, timestamp):
        self.cursor.execute('''
            INSERT INTO history(player_name, timestamp, score) VALUES(?, ?, ?)
        ''', (player_name, timestamp, score))
        self.connection.commit()

    def show_history(self):
        self.cursor.execute(
            '''SELECT * FROM history ORDER BY timestamp DESC''')
        return self.cursor.fetchall()

    async def get_total_score(self, player_name):
        self.cursor.execute('''
            SELECT SUM(score) FROM history WHERE player_name = ?
        ''', (player_name,))
        total_score = self.cursor.fetchone()[0]
        return total_score

    async def delete_latest_score(self, player_name):
        self.cursor.execute('''
            SELECT timestamp FROM history WHERE player_name = ? ORDER BY timestamp DESC LIMIT 1
        ''', (player_name,))
        latest_timestamp = self.cursor.fetchone()
        if latest_timestamp:
            timestamp = latest_timestamp[0]
            # 同じtimestampを持つすべてのレコードを削除
            self.cursor.execute('''
                DELETE FROM history WHERE timestamp = ?
            ''', (timestamp,))
            self.connection.commit()
            return f"同じtimestampを持つすべてのデータを削除しました。"
        else:
            return f"{player_name}のスコアは見つかりませんでした。"
