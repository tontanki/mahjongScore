import sqlite3


class HistoryData:
    def __init__(self, db_file='player_history.db'):
        self.db_file = db_file

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()
        self._create_table()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                player_id INTEGER,
                timestamp TEXT,
                score INTEGER,
                PRIMARY KEY (player_id, timestamp),
                FOREIGN KEY (player_id) REFERENCES players (player_id)
            )
        ''')
        # 既存のトリガーを削除
        self.cursor.execute('DROP TRIGGER IF EXISTS UpdatePlayerScore')

        self.cursor.execute('''
                CREATE TRIGGER UpdatePlayerScore AFTER INSERT ON history
                BEGIN
                    UPDATE scores
                    SET score = (SELECT SUM(score) FROM history WHERE player_id = NEW.player_id)
                    WHERE player_id = NEW.player_id;
                END;
            ''')
        self.connection.commit()

    async def insert_score(self, player_name, score, timestamp):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            player_id = self.get_player_id(player_name, cursor)
            if player_id:
                cursor.execute('''
                    INSERT INTO history(player_id, timestamp, score) VALUES(?, ?, ?)
                ''', (player_id, timestamp, score))
                conn.commit()
            else:
                raise ValueError(f"{player_name}は登録されていません")

    def show_history(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT players.player_name, history.timestamp, history.score
                FROM history
                JOIN players ON history.player_id = players.player_id
                ORDER BY history.timestamp DESC
                LIMIT 10
            ''')
            return cursor.fetchall()

    async def delete_latest_score(self, player_name):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            player_id = self.get_player_id(player_name, cursor)
            if player_id:
                cursor.execute('''
                    SELECT timestamp FROM history WHERE player_id = ? ORDER BY timestamp DESC LIMIT 1
                ''', (player_id,))
                latest_timestamp = cursor.fetchone()
                if latest_timestamp:
                    timestamp = latest_timestamp[0]
                    cursor.execute('''
                        DELETE FROM history WHERE timestamp = ?
                    ''', (timestamp,))
                    conn.commit()
                    return "同じtimestampを持つデータを削除しました。"
                else:
                    return "スコアは見つかりませんでした。"
            else:
                return "プレイヤーは登録されていません"

    def get_player_id(self, player_name, cursor=None):
        if cursor is None:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''SELECT player_id FROM players WHERE player_name=?''', (player_name,))
                result = cursor.fetchone()
        else:
            cursor.execute(
                '''SELECT player_id FROM players WHERE player_name=?''', (player_name,))
            result = cursor.fetchone()
        return result[0] if result else None

    def get_total_score(self, player_name):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            player_id = self.get_player_id(player_name, cursor)
            if player_id:
                cursor.execute(
                    '''SELECT SUM(score) FROM history WHERE player_id=?''', (player_id,))
                result = cursor.fetchone()
                return result[0] if result else 0
            else:
                raise ValueError(f"{player_name}は登録されていません")
