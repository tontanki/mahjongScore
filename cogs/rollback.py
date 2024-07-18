from discord.ext import commands
from player.player_data import PlayerData

player_data = PlayerData()


class RollbackCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='rollback')
    async def rollback_player(self, ctx, *args):
        """
        スコアについてロールバックする
        """
        if len(args) != 1:
            await ctx.send("プレイヤー名を正確に入力してください。")
            return

        player_name = args[0]
        message = player_data.rollback_player(player_name)

        if message:
            await ctx.send(message)
        else:
            await ctx.send("ロールバックしました。")


async def setup(bot):
    await bot.add_cog(RollbackCog(bot))
