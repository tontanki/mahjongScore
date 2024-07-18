from discord.ext import commands
from player.playerData import PlayerData

player_data = PlayerData()


class RollbackCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='rollback')
    async def rollback_player(self, ctx, *args):
        """
        スコアについてロールバックする
        """
        message = player_data.rollback_player(args)

        if message:
            await ctx.send(message)
        else:
            await ctx.send("ロールバックしました。")


async def setup(bot):
    await bot.add_cog(RollbackCog(bot))
