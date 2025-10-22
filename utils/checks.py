"""Custom checks for Discord bot commands."""
from discord.ext import commands


def is_in_voice_channel():
    """Check if the user is in a voice channel."""
    async def predicate(ctx):
        if not ctx.author.voice:
            await ctx.send("❌ You need to be in a voice channel to use this command!")
            return False
        return True
    return commands.check(predicate)


def is_bot_in_voice_channel():
    """Check if the bot is in a voice channel."""
    async def predicate(ctx):
        if not ctx.voice_client:
            await ctx.send("❌ The bot is not connected to a voice channel!")
            return False
        return True
    return commands.check(predicate)


def is_in_same_voice_channel():
    """Check if the user and bot are in the same voice channel."""
    async def predicate(ctx):
        if not ctx.author.voice:
            await ctx.send("❌ You need to be in a voice channel!")
            return False
        if ctx.voice_client and ctx.author.voice.channel != ctx.voice_client.channel:
            await ctx.send("❌ You need to be in the same voice channel as the bot!")
            return False
        return True
    return commands.check(predicate)




