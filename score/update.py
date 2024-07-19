from datetime import datetime
from db.history_data import HistoryData
from db.player_data import PlayerData


async def update_player_scores(scores):
    try:
        history = HistoryData()
        player_data = PlayerData()
        timestamp = datetime.timestamp(datetime.now())
        print(scores)
        for player, score in scores:
            print(player, score)
            await history.insert_score(player, score, timestamp)
            print(f"{player}のスコアを更新しました")
            total_score = await history.get_total_score(player)
            print(f"{player}の合計スコアは{total_score}です")
            await player_data.update_score(player, total_score)
            print(f"{player}のスコアを更新しました")

    except Exception as e:
        return f"エラーが発生しました: {e}"
