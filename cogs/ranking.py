from discord.ext import commands
from player.playerData import PlayerData


class RankingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = PlayerData()

    @commands.command(name='ranking')
    async def ranking_command(self, ctx):
        response = self.players.format_ranking()
        await ctx.send(response)

    @commands.command(name='delete_player')
    async def delete_player_command(self, ctx, player: str):
        self.players.delete_player(player)
        await ctx.send(f"{player} を削除しました。")


async def setup(bot):
    await bot.add_cog(RankingCog(bot))
