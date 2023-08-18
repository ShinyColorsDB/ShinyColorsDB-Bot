import discord
from discord import app_commands
from discord.ext import commands

from database import ScdbSeiyuu


class SeiyuuInfo(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Loaded cog 'seiyuuinfo'")

    async def seiyuuinfo_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str
    ) -> list[app_commands.Choice[str]]:
        return [app_commands.Choice(name=seiyuu.seiyuu_name, value=seiyuu.seiyuu_name)
                for seiyuu in ScdbSeiyuu.select().where((ScdbSeiyuu.seiyuu_name.contains(current))).limit(25)]

    @app_commands.command(name="seiyuuinfo", description="查詢聲優資料")
    @app_commands.describe(seiyuu="聲優姓名")
    @app_commands.autocomplete(seiyuu=seiyuuinfo_autocomplete)
    async def idolinfo(self, interaction: discord.Interaction, seiyuu: str):
        await interaction.response.defer()
        thisSeiyuu: ScdbSeiyuu = ScdbSeiyuu.get_or_none(
            ScdbSeiyuu.seiyuu_name == seiyuu)
        try:
            if thisSeiyuu == None:
                await interaction.followup.send("<:ml_serikapout:663075600503930880>")
                return

            embed = discord.Embed(
                title=thisSeiyuu.seiyuu_name,
            )
            # embed.set_thumbnail(url=thisSeiyuu.seiyuu_photo)
            embed.add_field(
                name="所屬", value=thisSeiyuu.belonging_firm)
            if thisSeiyuu.seiyuu_birth_year:
                embed.add_field(name="生年", value=thisSeiyuu.seiyuu_birth_year)
            embed.add_field(name="生日", value=thisSeiyuu.seiyuu_birth_date)
            if thisSeiyuu.seiyuu_twitter:
                embed.add_field(
                    name="Twitter", value=thisSeiyuu.seiyuu_twitter, inline=False)
            if thisSeiyuu.seiyuu_chokume:
                embed.add_field(
                    name="チョクメ", value=thisSeiyuu.seiyuu_chokume, inline=False)
            await interaction.followup.send(embed=embed)
        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(SeiyuuInfo(bot))
