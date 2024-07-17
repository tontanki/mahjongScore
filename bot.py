import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

scores = {}


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command()
# !score user1 25000 user2 30000 user3 35000
async def score(ctx, *args):
    global scores
    try:
        for i in range(0, len(args), 2):
            user = args[i]
            points = int(args[i + 1])
            scores[user] = points
        await ctx.send("スコアが更新されました。")
    except Exception as e:
        await ctx.send(f"エラーが発生しました: {e}")


@bot.command()
async def ranking(ctx, player_count: int):
    global scores
    if player_count not in [3, 4]:
        await ctx.send("プレイヤー数は3人または4人でなければなりません。")
        return

    base_score = 30000 if player_count == 4 else 40000

    ranking = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    response = "麻雀ランキング:\n"

    for i, (user, score) in enumerate(ranking, start=1):
        adjusted_score = (score - base_score) / 1000
        response += f"{i}. {user}: {score} 点 (調整後: {adjusted_score:.1f})\n"

    await ctx.send(response)
