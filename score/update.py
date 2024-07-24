from datetime import datetime
from db.history_data import HistoryData
from db.player_data import PlayerData


async def update_player_scores(scores):
    try:
        history = HistoryData()
        player_data = PlayerData()
        timestamp = datetime.timestamp(datetime.now())
        for player, score in scores:
            await history.insert_score(player, score, timestamp)
            await player_data.update_score(player)

    except Exception as e:
        return f"エラーが発生しました: {e}"
