from datetime import datetime
from player.history_data import HistoryData


async def update_player_scores(scores):
    try:
        history = HistoryData()
        timestamp = datetime.timestamp(datetime.now())
        for player, score in scores:
            await history.insert_score(player, score, timestamp)
    except Exception as e:
        return f"エラーが発生しました: {e}"
