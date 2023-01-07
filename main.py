import discord, asyncio, os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print("Bot ready\n")
    await bot.change_presence(activity=discord.Game(name="ShinyColorsDB-Bot /help"), status=discord.Status.online)


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
    await bot.start(os.environ.get("TOKEN"))

asyncio.run(main())
