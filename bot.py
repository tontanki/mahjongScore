import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ユーザー情報を保存する辞書
players = {}


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command()
async def score(ctx, *args):
    global players
    try:
        player_count = len(args) // 2  # 引数の数からプレイヤー数を計算
        base_score = 30000 if player_count == 4 else 40000

        most_points = max([int(args[i + 1]) for i in range(0, len(args), 2)])
        most_points_player = None
        sum_points = 0

        for i in range(0, len(args), 2):
            player = args[i]
            points = int(args[i + 1])

            # 最高点のプレイヤーはのちに計算
            if points == most_points:
                # すでにmost_points_playerが存在すればスキップ
                if most_points_player:
                    continue
                # 最高点のプレイヤーを記録
                most_points_player = player
                continue

            # 100で割って四捨五入する
            points = round(points / 100) * 100

            # ベーススコアを引いて合計点数に加算
            points = points - base_score
            points = round(points / 1000)
            sum_points += points

            if player in players:
                players[player] += points
            else:
                await ctx.send("プレイヤーが登録されていません。: " + player)

        players[most_points_player] += abs(sum_points)
        await ctx.send("スコアが更新されました。")
    except Exception as e:
        await ctx.send(f"エラーが発生しました: {e}")


@bot.command()
async def ranking(ctx):
    global players

    ranking = sorted(players.items(), key=lambda x: x[1], reverse=True)
    response = "麻雀ランキング:\n"

    for rank, (player, score) in enumerate(ranking, start=1):
        response += f"{rank}. {player}: {score}\n"

    await ctx.send(response)


@bot.command()
async def list_players(ctx):
    global players
    if not players:
        await ctx.send("現在登録されているユーザーはいません。")
    else:
        player_list = "\n".join(players.keys())
        await ctx.send(f"登録されているユーザー:\n{player_list}")


@bot.command()
async def register(ctx, *players_to_register: str):
    global players  # players変数をグローバルとして使用
    registered_players = []
    already_registered = []

    for player in players_to_register:
        if player in players:
            already_registered.append(player)
        else:
            players[player] = 0  # スコアを固定で0に設定
            registered_players.append(player)

    if registered_players:
        await ctx.send(f"{', '.join(registered_players)} を登録しました。")
    if already_registered:
        await ctx.send(f"{', '.join(already_registered)} はすでに登録されています。")


@bot.command()
async def delete_player(ctx, player: str):
    global players
    if player in players:
        del players[player]
        await ctx.send(f"{player} を登録から削除しました。")
    else:
        player_list = "\n".join(players.keys())
        await ctx.send(f"{player} は登録されていません。削除できません。")
        await ctx.send(f"登録されているユーザー:\n{player_list}")
