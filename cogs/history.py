from discord.ext import commands
from player.history_data import HistoryData
from tabulate import tabulate
from datetime import datetime


class HistoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.history = HistoryData()

    @commands.command(name='history')
    async def history_command(self, ctx):
        """
        スコアの履歴を見る
        """
        response = self.history.show_history()

        data = [(player, datetime.fromtimestamp(float(timestamp)).strftime('%Y-%m-%d %H:%M:%S'), score)
                for player, timestamp, score in response]

        history_message = tabulate(
            data, headers=["Player", "Timestamp", "Score"], tablefmt="grid")

        await ctx.send(f"```\n{history_message}\n```")


async def setup(bot):
    await bot.add_cog(HistoryCog(bot))
