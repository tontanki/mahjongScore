from discord.ext import commands
from player.player_data import PlayerData


class DeleteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='delete_player')
    async def delete_player_command(self, ctx, player: str):
        player_data = PlayerData()
        response = player_data.delete_player(player)
        await ctx.send(response)


async def setup(bot):
    await bot.add_cog(DeleteCog(bot))
