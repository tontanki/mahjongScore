from discord.ext import commands
from db.player_data import PlayerData
from tabulate import tabulate


class player_listCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = PlayerData()

    @commands.command(name='list')
    async def player_list_command(self, ctx):
        response = self.players.show_player_list()

    # データのリストを作成
        data = [(player, score) for player, score in response]

        # タブレートを使用して表を作成
        player_list_message = tabulate(
            data, headers=["Player", "Score"], tablefmt="grid")

        await ctx.send(f"\n```\n{player_list_message}\n```", silent=True)


async def setup(bot):
    await bot.add_cog(player_listCog(bot))
