from utils import update_data


async def update_player_scores(player, point):
    try:
        update_data(player, point)
    except Exception as e:
        return f"エラーが発生しました: {e}"
