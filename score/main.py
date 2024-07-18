from score.calculator import calculate_player_count, calculate_scores
from score.update import update_player_scores


async def update_scores(args):
    try:
        player_count = await calculate_player_count(args)
        await calculate_scores(args, player_count)
        return "スコアが更新されました。"
    except Exception as e:
        return f"エラーが発生しました: {e}"
