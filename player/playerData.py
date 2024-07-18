import json
import os


class PlayerData:
    def __init__(self, data_file='players_data.json'):
        self.data_file = data_file
        self.players = self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def refresh_data(self):
        self.players = self.load_data()

    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.players, f, ensure_ascii=False, indent=4)

    def update_data(self, player_name, score):
        if player_name in self.players:
            self.players[player_name] += score
        else:
            print("プレイヤー名がありません")
        self.save_data()

    def format_ranking(self):
        self.refresh_data()
        ranking = sorted(self.players.items(),
                         key=lambda x: x[1], reverse=True)
        if not ranking:
            return "プレイヤーが存在しません"
        response = "ランキング:\n"
        for rank, (player, score) in enumerate(ranking, start=1):
            response += f"{rank}. {player}: {score}\n"
        return response

    def register_player(self, *players_to_register):
        registered_players = []
        already_registered = []

        for player in players_to_register:
            if player in self.players:
                already_registered.append(player)
            else:
                self.players[player] = 0
                registered_players.append(player)

        if registered_players:
            self.save_data()

        return registered_players, already_registered

    def delete_player(self, *players_to_delete):
        deleted_players = []
        not_found_players = []

        for player in players_to_delete:
            if player in self.players:
                del self.players[player]  # プレイヤーを削除
                deleted_players.append(player)
            else:
                not_found_players.append(player)

        if deleted_players:
            self.save_data()  # 変更を保存

        return deleted_players, not_found_players
