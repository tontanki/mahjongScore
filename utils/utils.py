import json
import os

# データ保存用のファイルパス
data_file = 'players_data.json'


def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)


def save_data(players):
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(players, f, ensure_ascii=False, indent=4)


def update_data(player_name, score):
    players = load_data()
    if player_name in players:
        players[player_name] += score
    else:
        print("プレイヤー名がありません")


def format_ranking():
    global players
    """プレイヤーのスコアを降順にソートし、フォーマットされたランキング文字列を返す"""
    ranking = sorted(players.items(), key=lambda x: x[1], reverse=True)
    response = "ランキング:\n"
    for rank, (player, score) in enumerate(ranking, start=1):
        response += f"{rank}. {player}: {score}\n"
    return response
