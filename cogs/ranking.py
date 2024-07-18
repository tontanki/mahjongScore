from discord.ext import commands
from player.player_data import PlayerData
from tabulate import tabulate


class RankingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = PlayerData()

    @commands.command(name='ranking')
    async def ranking_command(self, ctx):
        response = self.players.show_ranking()

    # データのリストを作成
        data = [(player, score) for player, score in response]

        # タブレートを使用して表を作成
        ranking_message = tabulate(
            data, headers=["Player", "Score"], tablefmt="grid")

        await ctx.send(f"```\n{ranking_message}\n```")


async def setup(bot):
    await bot.add_cog(RankingCog(bot))
