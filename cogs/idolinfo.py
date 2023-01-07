import discord
from discord import app_commands
from discord.ext import commands

from database import ScdbIdols

class IdolInfo(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Loaded cog 'idolinfo'")

    async def idolinfo_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str
    ) -> list[app_commands.Choice[str]]:
        return [app_commands.Choice(name=idol.idol_name, value=idol.idol_name)
            for idol in ScdbIdols.select().where((ScdbIdols.idol_name.contains(current)) & (ScdbIdols.idol_id != 0) & (ScdbIdols.idol_id != 26)).limit(25)]

    @app_commands.command(name="idolinfo", description="查詢偶像資料")
    @app_commands.describe(idols="偶像名稱")
    @app_commands.autocomplete(idols=idolinfo_autocomplete)
    async def idolinfo(self, interaction: discord.Interaction, idols: str):
        await interaction.response.defer()
        thisIdol = ScdbIdols.get(ScdbIdols.idol_name == idols)
        try:
            embed = discord.Embed(
                title=thisIdol.idol_name,
                url=f"https://shinycolors.moe/idolinfo?idolid={thisIdol.idol_id}",
                color=discord.Colour.from_str(thisIdol.color1)
            )
            embed.add_field(name="ひらがな", value=thisIdol.hiragana)
            embed.add_field(
                name="所屬", value=thisIdol.unit.unit_name)
            embed.add_field(name="年齡", value=thisIdol.age)
            embed.add_field(name="生日", value=thisIdol.birthday)
            embed.add_field(name="身長", value=thisIdol.height)
            embed.add_field(name="体重", value=thisIdol.weight)
            embed.add_field(name="スリーサイズ", value=thisIdol.three_size)
            embed.add_field(name="星座", value=thisIdol.star_sign)
            embed.add_field(name="血型", value=thisIdol.blood_type)
            embed.add_field(name="趣味", value=thisIdol.interest, inline=False)
            embed.add_field(name="特技", value=thisIdol.special_skill, inline=False)
            embed.add_field(name="CV", value=thisIdol.cv, inline=False)
            embed.set_image(
                url=f'https://static.shinycolors.moe/pictures/icon/{str(thisIdol.idol_id).zfill(2)}.jpg')
        except Exception as e:
            print(e)
        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(IdolInfo(bot))
