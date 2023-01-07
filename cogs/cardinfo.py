import discord
from discord import app_commands
from discord.ext import commands

from database import ScdbCardList

class CardInfo(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Loaded cog 'cardinfo'")

    async def cardinfo_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str
    ) -> list[app_commands.Choice[str]]:
        return [app_commands.Choice(name=card.card_name, value=card.card_name)
                       for card in ScdbCardList.select().where(ScdbCardList.card_name.contains(current)).limit(25)]

    @app_commands.command(name="cardinfo", description="查詢卡片資料")
    @app_commands.describe(cardname="卡片名稱")
    @app_commands.autocomplete(cardname=cardinfo_autocomplete)
    async def cardinfo(self, interaction: discord.Interaction, cardname: str):
        await interaction.response.defer()
        thisCard = ScdbCardList.get(ScdbCardList.card_name == cardname)

        try:
            ps = "p" if "P_" in thisCard.card_type else "s"
            embed = discord.Embed(
                title=thisCard.card_name,
                color=discord.Colour.from_str(thisCard.idol.color1),
                url=f"https://shinycolors.moe/{ps}cardinfo?uuid={thisCard.card_uuid}"
            )
            if "P_" in thisCard.card_type:
                embed.set_image(
                    url=f"https://static.shinycolors.moe/pictures/bigPic/{thisCard.big_pic2}.jpg")
            else:
                embed.set_image(
                    url=f"https://static.shinycolors.moe/pictures/bigPic/{thisCard.big_pic1}.jpg")
            embed.set_thumbnail(
                url=f"https://static.shinycolors.moe/pictures/smlPic/{thisCard.sml_pic}.png")
            embed.add_field(name="類別", value=thisCard.card_type)
            embed.add_field(name="取得方式", value=thisCard.get_method)
            embed.add_field(name="實裝日期", value=thisCard.release_date)

        except Exception as e:
            print(e)

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CardInfo(bot))
