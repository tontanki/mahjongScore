from player.playerData import PlayerData


async def update_player_scores(player, point):
    try:
        player_data = PlayerData()
        player_data.update_data(player, point)
    except Exception as e:
        return f"エラーが発生しました: {e}"
