import sqlite3


class PlayerData:
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
            CREATE TABLE IF NOT EXISTS players (
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT UNIQUE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                player_id INTEGER,
                score INTEGER,
                FOREIGN KEY (player_id) REFERENCES players (player_id)
            )
        ''')
        self.connection.commit()

    def register_player(self, *players_name):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            registered_players = []
            already_registered = []

            for player_name in players_name:
                cursor.execute(
                    '''SELECT player_id FROM players WHERE player_name=?''', (player_name,))
                result = cursor.fetchone()

                if result:
                    already_registered.append(player_name)
                else:
                    cursor.execute(
                        '''INSERT INTO players(player_name) VALUES(?)''', (player_name,))
                    player_id = cursor.lastrowid
                    cursor.execute(
                        '''INSERT INTO scores(player_id, score) VALUES(?, ?)''', (player_id, 0))
                    registered_players.append(player_name)

            self.connection.commit()
            return registered_players, already_registered

    def show_player_list(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT players.player_name, scores.score
                FROM scores
                JOIN players ON scores.player_id = players.player_id
                ORDER BY scores.score DESC
            ''')
            return cursor.fetchall()

    def delete_player(self, player_name):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT player_id FROM players WHERE player_name=?''', (player_name,))
            result = cursor.fetchone()
            if result:
                player_id = result[0]
                cursor.execute(
                    '''DELETE FROM players WHERE player_id=?''', (player_id,))
                cursor.execute(
                    '''DELETE FROM scores WHERE player_id=?''', (player_id,))
                cursor.execute(
                    '''DELETE FROM history WHERE player_id=?''', (player_id,))
                self.connection.commit()
                return f"{player_name}を削除しました"
            else:
                return f"{player_name}は登録されていません"

    def get_player_id(self, player_name):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT player_id FROM players WHERE player_name=?''', (player_name,))
            result = cursor.fetchone()
            return result[0] if result else None

    def is_registered(self, player_name):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor
            cursor.execute(
                '''SELECT player_id FROM players WHERE player_name=?''', (player_name,))
            return bool(cursor.fetchone())
