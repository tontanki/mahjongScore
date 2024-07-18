from discord.ext import commands
from score.main import update_scores


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

        result = await update_scores(args)
        await ctx.send(result)


async def setup(bot):
    await bot.add_cog(ScoreCog(bot))
