from score.update import update_player_scores
import datetime


async def calculate_player_count(args):
    return len(args) // 2


async def calculate_scores(args, player_count):
    base_score = 30000 if player_count == 4 else 40000
    most_points = max([int(args[i + 1]) for i in range(0, len(args), 2)])
    most_points_player = None
    sum_points = 0
    scores = []

    for i in range(0, len(args), 2):
        player = args[i]
        points = int(args[i + 1])

        if points == most_points:
            if not most_points_player:
                most_points_player = player
            continue

        points = round(points / 100) * 100
        points = points - base_score
        points = round(points / 1000)
        sum_points += points

        scores.append((player, points))

    scores.append((most_points_player, abs(sum_points)))
    return scores
