from player.player_data import PlayerData


async def update_player_scores(player, point, timestamp):
    try:
        player_data = PlayerData()
        player_data.update_data(player, point, timestamp)
    except Exception as e:
        return f"エラーが発生しました: {e}"
