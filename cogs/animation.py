import os, datetime, pytz
from discord.ext import commands, tasks

class Animation(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.animationUpdate.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Loaded cog 'animation'")

    def cog_unload(self):
        self.animationUpdate.cancel()

    @tasks.loop(time=datetime.time(hour=1, minute=0, second=0, tzinfo=pytz.timezone('Asia/Taipei')))
    async def animationUpdate(self):
        return
        if datetime.datetime.now(pytz.timezone('Asia/Taipei')).weekday() == 5:
            for cId in os.environ.get("NOTIFY").split(","):
                channel = self.bot.get_channel(int(cId))
                await channel.send("蝦泥阿尼更新拉，快打開哈哈姆特卡通瘋!")

    @animationUpdate.before_loop
    async def before_animation(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Animation(bot))
