import discord
import os
from discord.ext import commands, ipc
from settings import token
from utils.CustomBot import CustomBot

bot = CustomBot(command_prefix="!",
                intents = discord.Intents.all(),
                allowed_mentions = discord.AllowedMentions().none(),
                activity = discord.Activity(type = discord.ActivityType.listening, name = "!help | !rank"),
                case_insensitive = True)
bot.embed_color = 0x2F3136
startup_extensions = ['cogs.help', 'jishaku', 'cogs.errors', 'cogs.owner', 'cogs.ranks', 'cogs.listener', 'cogs.etc', 'cogs.moderator']

#Add jsk things
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

@bot.event
async def on_ready():
    print(f"Bot is ready")
    print("-" * 10)

#Load cogs
if __name__ == "__main__":
    bot.ipc.start()
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run(token())
