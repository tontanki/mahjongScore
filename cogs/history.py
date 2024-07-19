from discord.ext import commands
from player.history_data import HistoryData


class HistoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='history')
    async def history_command(self, ctx):
        """
        スコアの履歴を見る
        """
        history = HistoryData()
        result = history.show_history()
        await ctx.send(result)


async def setup(bot):
    await bot.add_cog(HistoryCog(bot))
