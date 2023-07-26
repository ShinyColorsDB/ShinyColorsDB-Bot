import os, datetime, pytz
from discord.ext import commands, tasks

from database import ScdbIdols

class Birthday(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.birthday.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Loaded cog 'birthday'")

    def cog_unload(self):
        self.birthday.cancel()

    @tasks.loop(time=datetime.time(hour=0, minute=0, second=0, tzinfo=pytz.timezone('Asia/Tokyo')))
    #@tasks.loop(seconds=10)
    async def birthday(self):
        for idol in ScdbIdols.select().where(ScdbIdols.birthday == datetime.datetime.now(
                pytz.timezone('Asia/Tokyo')).strftime("%m/%d")):
            for cId in os.environ.get("NOTIFY").split(","):
                channel = self.bot.get_channel(int(cId))
                await channel.send(idol.idol_name + "の誕生日です！")

    @birthday.before_loop
    async def before_birthday(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Birthday(bot))
