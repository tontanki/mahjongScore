from datetime import datetime
from player.history_data import HistoryData
from player.player_data import PlayerData


async def update_player_scores(scores):
    try:
        print(f"Scores: {scores}")
        history = HistoryData()
        player_data = PlayerData()
        timestamp = datetime.timestamp(datetime.now())
        for player, score in scores:
            await history.insert_score(player, score, timestamp)
            total_score = await history.get_total_score(player)
            print(f"Player: {player}, Score: {
                score}, Total Score: {total_score}")
            await player_data.update_score(player, total_score)

    except Exception as e:
        return f"エラーが発生しました: {e}"
