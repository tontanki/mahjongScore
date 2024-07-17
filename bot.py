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
        for i in range(0, len(args), 2):
            player = args[i]
            points = int(args[i + 1])
            if player in players:
                players[player] += points
            else:
                players[player] = points
        await ctx.send("スコアが更新されました。")
    except Exception as e:
        await ctx.send(f"エラーが発生しました: {e}")


@bot.command()
async def ranking(ctx, player_count: int):
    global players
    if player_count not in [3, 4]:
        await ctx.send("プレイヤー数は3人または4人でなければなりません。")
        return

    base_score = 30000 if player_count == 4 else 40000

    ranking = sorted(players.items(), key=lambda x: x[1], reverse=True)
    response = "麻雀ランキング:\n"

    for i, (player, score) in enumerate(ranking, start=1):
        adjusted_score = (score - base_score) / 1000
        response += f"{i}. {player}: {score} 点 (調整後: {adjusted_score:.1f})\n"

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
async def register(ctx, player: str):
    global players  # players変数をグローバルとして使用
    if player in players:
        await ctx.send(f"{player} はすでに登録されています。")
    else:
        players[player] = 0  # スコアを固定で0に設定
        await ctx.send(f"{player} を登録しました。")


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
