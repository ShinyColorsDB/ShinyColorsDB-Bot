import discord
from discord import app_commands
from discord.ext import commands

from database import ScdbCardList

class EventInfo(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Loaded cog 'eventInfo'")

    async def eventinfo_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str
    ) -> list[app_commands.Choice[str]]:
        return [app_commands.Choice(name=card.card_name, value=card.card_name)
                for card in ScdbCardList.select().where(ScdbCardList.card_name.contains(current)).order_by(ScdbCardList.enza_id.asc()).limit(25)]

    @app_commands.command(name="eventinfo", description="查詢卡片資料")
    @app_commands.describe(eventname="卡片名稱")
    # @app_commands.autocomplete(eventname=eventinfo_autocomplete)
    async def eventinfo(self, interaction: discord.Interaction, eventname: str):
        await interaction.response.defer()

        await interaction.followup.send("<:ml_serikapout:663075600503930880>")


async def setup(bot):
    await bot.add_cog(EventInfo(bot))
