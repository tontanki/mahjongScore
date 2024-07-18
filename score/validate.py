def validate_scores(input_str):
    # 入力文字列をリストとして受け取って使用する
    parts = input_str

    # スコアのみを抽出（偶数インデックスはプレイヤー名なのでスキップ）
    scores = [parts[i] for i in range(1, len(parts), 2)]

    # スコアが全て数値であるか確認
    if not all(s.lstrip('-').isdigit() for s in scores):
        raise ValueError("スコアは全て数値でなければなりません。")

    # 数値に変換
    scores = [int(s) for s in scores]

    # マイナスの数値を考慮して合計スコアの検証
    total_score = sum(scores)
    if (len(scores) == 4 and total_score != 100000) or (len(scores) == 3 and total_score != 105000):
        raise ValueError("合計スコアが不正です。")

    # 1と2の位が0かどうかを確認
    if any(s % 100 != 0 for s in scores):
        raise ValueError("スコアは100の倍数でなければなりません。")
