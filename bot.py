import discord
from discord.ext import commands
from player.playerData import PlayerData

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

players = PlayerData()


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command()
async def ranking(ctx):  # ランキングを表示するコマンド
    response = players.format_ranking()
    await ctx.send(response)


@bot.command()
async def register(ctx, *players_to_register: str):
    player_data = PlayerData()  # PlayerDataインスタンスを作成または参照
    registered_players, already_registered = player_data.register_player(
        *players_to_register)

    if registered_players:
        await ctx.send(f"{', '.join(registered_players)} を登録しました。")
    if already_registered:
        await ctx.send(f"{', '.join(already_registered)} はすでに登録されています。")


@bot.command()
async def delete_player(ctx, player: str):
    global players
    if player in players:
        del players[player]
        save_data()
        await ctx.send(f"{player} を登録から削除しました。")
    else:
        player_list = "\n".join(players.keys())
        await ctx.send(f"{player} は登録されていません。削除できません。")
        await ctx.send(f"登録されているユーザー:\n{player_list}")
