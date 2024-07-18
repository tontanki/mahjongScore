import json
import os


class PlayerData:
    def __init__(self, data_file='players_data.json'):
        self.data_file = data_file
        self.players = self._load_data()

    def _load_data(self):
        """プレイヤーデータをファイルから読み込む。ファイルが存在しない場合、空の辞書を返す。"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_data(self):
        """現在のプレイヤーデータをファイルに保存する。"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.players, f, ensure_ascii=False, indent=4)

    def update_data(self, player_name, score):
        """指定されたプレイヤーのスコアを更新する。プレイヤーが存在しない場合、メッセージを表示する。"""
        if player_name in self.players:
            self.players[player_name] += score
        else:
            print("プレイヤー名がありません")
        self._save_data()

    def format_ranking(self):
        """プレイヤーのランキングをフォーマットして返す。"""
        self.players = self._load_data()
        ranking = sorted(self.players.items(),
                         key=lambda x: x[1], reverse=True)
        if not ranking:
            return "プレイヤーが存在しません"

        response = "ランキング:\n"
        for rank, (player, score) in enumerate(ranking, start=1):
            response += f"{rank}. {player}: {score}\n"
        return response

    def register_player(self, *players_to_register):
        """新しいプレイヤーを登録する。すでに登録されているプレイヤーをチェックし、それに応じたリストを返す。"""
        registered_players = []
        already_registered = []

        for player in players_to_register:
            if player in self.players:
                already_registered.append(player)
            else:
                self.players[player] = 0
                registered_players.append(player)

        if registered_players:
            self._save_data()

        return registered_players, already_registered

    def delete_player(self, *players_to_delete):
        """指定されたプレイヤーを削除する。存在しないプレイヤーをチェックし、それに応じたリストを返す。"""
        deleted_players = []
        not_found_players = []

        for player in players_to_delete:
            if player in self.players:
                del self.players[player]
                deleted_players.append(player)
            else:
                not_found_players.append(player)

        if deleted_players:
            self._save_data()

        return deleted_players, not_found_players
