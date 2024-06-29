import discord
from discord import app_commands
from discord.ext import commands

class Pout(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Loaded cog 'pout'")

    @app_commands.command(name="pout", description="星梨花不爽")
    @app_commands.describe(count="重複數量")
    @app_commands.allowed_installs(users=True, guilds=True)
    async def pout(self, interaction: discord.Interaction, count: int = 1):
        await interaction.response.defer()
        pouts = "<:ml_serikapout:663075600503930880>"
        if count <= 10 and count > 0:
            for _ in range(count - 1):
                pouts += "<:ml_serikapout:663075600503930880>"
        await interaction.followup.send(pouts)

async def setup(bot):
    await bot.add_cog(Pout(bot))
