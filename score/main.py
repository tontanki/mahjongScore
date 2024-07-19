from score.calculator import calculate_player_count, calculate_scores
from score.validate import validate_scores
from score.update import update_player_scores


async def update_scores(args):
    try:
        validate_scores(args)
        player_count = await calculate_player_count(args)
        scores = await calculate_scores(args, player_count)
        await update_player_scores(scores)

    except Exception as e:
        return f"エラーが発生しました: {e}"
