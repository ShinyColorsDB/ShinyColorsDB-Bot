import discord
from discord import app_commands
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Loaded cog 'help'")

    @app_commands.command(name="help", description="使用指南")
    async def help(self, interaction: discord.Interaction):
        await interaction.response.defer()

        embed = discord.Embed(
            title="ShinyColorsDB-Bot /help",
            color=discord.Colour.blue()
        )

        embed.add_field(name="/idolinfo", value="查詢偶像資料", inline=False)
        embed.add_field(name="/cardinfo", value="查詢卡片資料", inline=False)
        embed.add_field(name="/pout", value="星梨花不爽", inline=False)
        embed.add_field(name="/help", value="使用指南", inline=False)

        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
