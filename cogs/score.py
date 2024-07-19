from discord.ext import commands
from score.main import update_scores
from player.history_data import HistoryData
from score.update import update_player_scores


class ScoreCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='score')
    async def score_command(self, ctx, *args):
        """
        スコアの計算をする。
        !score playerNAME scoreNUM playerNAME scoreNUM ...
        3人分なら4万点返し、4人分なら3万点返しをする。 
        """
        try:
            result = await update_scores(args)
            if result:
                await ctx.send(result)
            else:
                await ctx.send(f"スコアを更新しました。")
        except Exception as e:
            await ctx.send(f"エラーが発生しました: {e}")


async def setup(bot):
    await bot.add_cog(ScoreCog(bot))
