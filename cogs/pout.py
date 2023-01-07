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
    async def pout(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send("<:ml_serikapout:663075600503930880>")

async def setup(bot):
    await bot.add_cog(Pout(bot))
