from discord.ext import commands
from player.player_data import PlayerData


class RegisterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='register')  # コマンド名をここで指定
    async def register_command(self, ctx, *players_to_register):
        player_data = PlayerData()  # PlayerDataインスタンスを作成または参照
        registered_players, already_registered = player_data.register_player(
            *players_to_register)

        if registered_players:
            await ctx.send(f"{', '.join(registered_players)} を登録しました。")
        if already_registered:
            await ctx.send(f"{', '.join(already_registered)} はすでに登録されています。")


async def setup(bot):
    await bot.add_cog(RegisterCog(bot))