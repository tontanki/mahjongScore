from score.calculator import calculate_player_count, calculate_scores
from score.validate import validate_scores


async def update_scores(args):
    try:
        validate_scores(args)
        player_count = await calculate_player_count(args)
        return await calculate_scores(args, player_count)

    except Exception as e:
        return f"エラーが発生しました: {e}"
