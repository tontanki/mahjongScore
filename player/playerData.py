import json
import os
from datetime import datetime


class PlayerData:
    def __init__(self, data_file='players_data.json', history_file='players_history.json'):
        self.data_file = data_file
        self.history_file = history_file
        self.players = self._load_data()
        self.history = self._load_history()

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

    def _load_history(self):
        """プレイヤーの履歴データをファイルから読み込む。ファイルが存在しない場合、空の辞書を返す。"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_history(self):
        """現在のプレイヤー履歴データをファイルに保存する。"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def _log_history(self, player_name, score):
        """プレイヤーのスコア変更を履歴に記録する。"""
        if player_name not in self.history:
            self.history[player_name] = []
        self.history[player_name].append({
            'timestamp': datetime.now().isoformat(),
            'score': score,
            'total_score': self.players.get(player_name, 0)
        })
        self._save_history()

    def update_data(self, player_name, score):
        """指定されたプレイヤーのスコアを更新する。プレイヤーが存在しない場合、メッセージを表示する。"""
        if player_name in self.players:
            self.players[player_name] += score
            self._log_history(player_name, score)
            self._save_data()
        else:
            print("プレイヤー名がありません")

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

    def rollback_player(self, player_name):
        """プレイヤーのスコアを最新の履歴を削除してロールバックする。"""
        if player_name not in self.history:
            return "履歴が見つかりません"

        history = self.history[player_name]
        if len(history) > 1:
            # 最新の履歴を削除
            del history[-1]
            # 削除後の最新の履歴を取得
            rollback_point = history[-1]
            self.players[player_name] = rollback_point['total_score']
            self._save_data()
        elif len(history) == 1:
            # 履歴が1つしかない場合は、その履歴を削除してスコアを0にリセット
            del history[-1]
            self.players[player_name] = 0
            self._save_data()
        else:
            return "ロールバックする履歴がありません"

    def print_all_players_history(self):
        """全プレイヤーのスコア履歴をきれいに整形して文字列で返す。"""
        if not self.history:
            return "履歴が存在しません"

        response = ""
        for player, history in self.history.items():
            response += f"{player} :\n"
            for idx, entry in enumerate(history, start=1):
                response += f"\t{idx}\n"
                response += f"\t\tscore : {entry['score']}\n"
                response += f"\t\ttotal_score : {entry['total_score']}\n"

        return response
