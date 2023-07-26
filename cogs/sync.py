import os
from discord import app_commands
from discord.ext import commands

class Sync(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command()
    async def sync(self, ctx) -> None:
        if not (str(ctx.message.author) == str(os.environ.get("OWNER"))):
            return

        fmt = await ctx.bot.tree.sync()
        await ctx.send(f"Syncd {len(fmt)} commands to all guild")

async def setup(bot):
    await bot.add_cog(Sync(bot))
