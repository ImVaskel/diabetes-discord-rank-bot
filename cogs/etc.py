import discord
from discord.ext import commands
from discord.ext.commands import BucketType
from jishaku.codeblocks import codeblock_converter
import mystbin

class EtcCog(commands.Cog, name = "etc"):
    def __init__(self, bot):
        self.bot = bot
        self.mystbin = mystbin.Client()

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! Latency is `{round(self.bot.latency*1000)}`ms")

    @commands.command()
    async def github(self, ctx):
        """Links to the github"""
        embed = discord.Embed(title = "GitHub", color = self.bot.embed_color)

        embed.add_field(name = "__**Issues**__", value = "https://github.com/ImVaskel/diabetes-discord-rank-bot/issues/new")

        await ctx.send(embed = embed)

    @commands.command()
    async def license(self, ctx):
        await ctx.send(embed = discord.Embed(description="https://github.com/ImVaskel/diabetes-discord-rank-bot/blob/master/LICENSE"))

    @commands.command(aliases=["mystbin"])
    @commands.cooldown(1, 30, BucketType.user)
    async def paste(self, ctx, paste: str = None):
        """Pastes a file to mystbin, attempts to check for an attachment first, and if it cannot detect one, goes to text, and will error if it can't find that. You can also use codeblocks and it will detect text in that. Detects file extension."""
        if not paste and not ctx.message.attachments:
            return await ctx.send("You didn't provide anything to paste")

        # Checking for attachment first
        elif not paste:
            attachments = ctx.message.attachments
            if attachments[0].height:
                return await ctx.send(
                    "That file has a height, meaning it's probably an image. I can't paste those!")

            if attachments[0].size // 1000000 > 8:
                return await ctx.send("That's too large of a file!")

            split_attachment = attachments[0].filename.split(".")

            if split_attachment[1] in ["zip", "exe", "nbt"]:
                return await ctx.send(
                    f"Invalid file type: `{split_attachment[1]}` is invalid.")

            file = await attachments[0].read()
            text = file.decode('UTF-8')
            url = await self.mystbin.post(text, syntax=split_attachment[1])

            return await ctx.send(str(url))

        # Checking for text
        elif not ctx.message.attachments:
            paste = codeblock_converter(paste)
            url = await self.mystbin.post(paste[1], syntax=paste[0])
            return await ctx.send(str(url))

def setup(bot):
    bot.add_cog(EtcCog(bot))