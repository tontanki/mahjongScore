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

    def insert_score(self, player_name, timestamp, score):
        # Check if player already exists for the given timestamp
        self.cursor.execute('''
            SELECT * FROM scores
            WHERE player_name=? AND timestamp=?
        ''', (player_name, timestamp))
        existing_entry = self.cursor.fetchone()

        if existing_entry:
            # Update existing entry
            new_total_score = existing_entry[3] + score
            self.cursor.execute('''
                UPDATE scores
                SET score=?, total_score=?
                WHERE player_name=? AND timestamp=?
            ''', (score, new_total_score, player_name, timestamp))
        else:
            # Insert new entry
            new_total_score = score
            self.cursor.execute('''
                INSERT INTO scores(player_name, timestamp, score, total_score)
                VALUES(?, ?, ?, ?)
            ''', (player_name, timestamp, score, new_total_score))

        self.connection.commit()

    def delete_scores_by_timestamp(self, timestamp):
        # Retrieve all player names with the given timestamp
        self.cursor.execute('''
            SELECT DISTINCT player_name FROM scores
            WHERE timestamp=?
        ''', (timestamp,))
        players_to_delete = [row[0] for row in self.cursor.fetchall()]

        # Delete entries for each player with the given timestamp
        self.cursor.execute('''
            DELETE FROM scores
            WHERE timestamp=?
        ''', (timestamp,))
        self.connection.commit()

        return players_to_delete

    def get_total_score(self, player_name, timestamp):
        # Retrieve total score for a player at a specific timestamp
        self.cursor.execute('''
            SELECT total_score FROM scores
            WHERE player_name=? AND timestamp=?
        ''', (player_name, timestamp))
        result = self.cursor.fetchone()

        if result:
            return result[0]
        else:
            return None

    def close_connection(self):
        self.connection.close()
