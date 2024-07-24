from db.player_data import PlayerData
player_data = PlayerData()


def validate_scores(parts):
    # 入力が3回または4回のペアであることを確認
    if len(parts) not in [6, 8]:
        raise ValueError("入力はplayer_nameとNUMのペアで3回または4回でなければなりません。")

    # プレイヤー名を抽出
    player_names = [parts[i] for i in range(0, len(parts), 2)]

    # プレイヤー名の重複をチェック
    if len(player_names) != len(set(player_names)):
        raise ValueError("プレイヤー名が重複しています。")

    # プレイヤー名が存在するか確認
    for player_name in player_names:
        if not player_data.is_registered(player_name):
            raise ValueError(f"{player_name} は登録されていません。")

        # 入力をプレイヤー名とスコアのリストとして受け取る
    scores = [parts[i] for i in range(1, len(parts), 2)]

    # スコアが全て数値であるか確認し、数値に変換
    try:
        scores = [int(s) for s in scores]
    except ValueError:
        raise ValueError("スコアは全て数値でなければなりません。")

    # 合計スコアの検証
    total_score = sum(scores)
    expected_total = 100000 if len(scores) == 4 else 105000
    if total_score != expected_total:
        raise ValueError(f"合計スコアが不正です。期待値: {
                         expected_total}, 実際: {total_score}")

    # スコアが100の倍数であるかを確認
    if any(s % 100 != 0 for s in scores):
        raise ValueError("スコアは100の倍数でなければなりません。")
