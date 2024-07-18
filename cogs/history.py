from discord.ext import commands
from player.playerData import PlayerData

player_data = PlayerData()


class HistoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='history')
    async def history_command(self, ctx):
        """
        スコアの履歴を見る
        """
        result = player_data.print_all_players_history()
        await ctx.send(result)


async def setup(bot):
    await bot.add_cog(HistoryCog(bot))
