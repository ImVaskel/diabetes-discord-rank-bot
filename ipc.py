import discord
from discord.ext import commands, ipc

class IpcCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(IpcCog(bot))