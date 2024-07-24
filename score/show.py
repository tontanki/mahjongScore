async def show_scores(ctx, scores):
    for player, score in scores:
        await ctx.send(f"{player}: {score} 点", silent=True)
