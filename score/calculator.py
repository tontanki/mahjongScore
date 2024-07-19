async def calculate_player_count(args):
    return len(args) // 2


async def calculate_scores(args, player_count):
    base_score = 30000 if player_count == 4 else 40000
    player_points = [(args[i], int(args[i + 1]))
                     for i in range(0, len(args), 2)]
    most_points = max(points for _, points in player_points)
    most_points_player = next(
        player for player, points in player_points if points == most_points)
    sum_points = 0
    scores = []

    for player, points in player_points:
        if points == most_points:
            continue

        points = round(points / 100) * 100
        points = round((points - base_score) / 1000)
        sum_points += points
        scores.append((player, points))

    scores.append((most_points_player, -sum_points))
    return scores
