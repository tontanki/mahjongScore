import sqlite3
import json
from datetime import datetime


class PlayerData:
    def __init__(self, db_file='players.db'):
        self.db_file = db_file
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                player_name TEXT,
                score INTEGER,
                PRIMARY KEY (player_name)
            )
        ''')
        self.connection.commit()

    def register_player(self, *players_name):
        registered_players = []  # 登録したプレイヤー
        already_registered = []  # 登録済みのプレイヤー

        for player_name in players_name:
            self.cursor.execute(
                '''SELECT * FROM scores WHERE player_name=?''', (player_name,))  # ?(プレースホルダー)
            # fetchone()で結果を取得
            result = self.cursor.fetchone()

            if result:
                already_registered.append(player_name)
            else:
                self.cursor.execute('''INSERT INTO scores(player_name, score) VALUES(?, ?)''',
                                    (player_name, 0))
                registered_players.append(player_name)

        self.connection.commit()
        return registered_players, already_registered

    def show_ranking(self):
        self.cursor.execute('''SELECT * FROM scores ORDER BY score DESC''')
        return self.cursor.fetchall()

    def delete_player(self, player_name):
        self.cursor.execute(
            '''SELECT * FROM scores WHERE player_name=?''', (player_name,))
        result = self.cursor.fetchone()
        if result:
            self.cursor.execute(
                '''DELETE FROM scores WHERE player_name=?''', (player_name,))
            self.connection.commit()
            return f"{player_name}を削除しました"
        else:
            return f"{player_name}は登録されていません"

    async def update_score(self, player_name, score):
        self.cursor.execute(
            '''SELECT * FROM scores WHERE player_name=?''', (player_name,))
        result = self.cursor.fetchone()
        if result:
            self.cursor.execute(
                '''UPDATE scores SET score=? WHERE player_name=?''', (score, player_name))
            self.connection.commit()
            return f"{player_name}のスコアを{score}に更新しました"
        else:
            return f"{player_name}は登録されていません"
