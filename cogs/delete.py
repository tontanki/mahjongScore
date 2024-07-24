from discord.ext import commands
from db.player_data import PlayerData
from db.history_data import HistoryData


class DeleteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='delete_player')
    async def delete_player_command(self, ctx, player: str):
        player_data = PlayerData()
        response = player_data.delete_player(player)
        await ctx.send(response, silent=True)

    @commands.command(name='delete_score')
    async def delete_score_command(self, ctx, player: str):
        history = HistoryData()
        response = await history.delete_latest_score(player)
        await ctx.send(response, silent=True)


async def setup(bot):
    await bot.add_cog(DeleteCog(bot))
