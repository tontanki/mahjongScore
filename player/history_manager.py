# history_manager.py

import json
import os
from datetime import datetime


class HistoryManager:
    def __init__(self, history_file='players_history.json'):
        self.history_file = history_file
        self.history = self._load_history()

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

    def _log_history(self, player_name, score, players_data):
        """プレイヤーのスコア変更を履歴に記録する。"""
        if player_name not in self.history:
            self.history[player_name] = []
        self.history[player_name].append({
            'timestamp': datetime.now().isoformat(),
            'score': score,
            'total_score': players_data.players.get(player_name, 0)
        })
        self._save_history()

    def rollback_player(self, player_name, players_data):
        """プレイヤーのスコアを最新の履歴を削除してロールバックする。"""
        if player_name not in self.history or not self.history[player_name]:
            return f"{player_name} の履歴が見つかりません"

        history = self.history[player_name]
        if len(history) > 1:
            # 最新の履歴を削除
            del history[-1]
            # 削除後の最新の履歴を取得
            rollback_point = history[-1]
            players_data.players[player_name] = rollback_point['total_score']
            players_data._save_data()
        elif len(history) == 1:
            # 履歴が1つしかない場合は、その履歴を削除してスコアを0にリセット
            del history[-1]
            players_data.players[player_name] = 0
            players_data._save_data()
        else:
            return "ロールバックする履歴がありません"

        # 履歴が空になった場合、self.historyから削除する
        if not self.history[player_name]:
            del self.history[player_name]
            self._save_history()

        return f"{player_name} の最新の履歴を削除し、ロールバックしました."

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


if __name__ == "__main__":
    # テストコードなどをここに追加
    pass
