"""Discord bot initialization and cog loading."""
import os
import asyncio
import discord
from discord.ext import commands
from utils.config import BOT_PREFIX, get_bot_intents, DISCORD_TOKEN


class MusicBot(commands.Bot):
    """Custom Discord bot class for the music bot."""
    
    def __init__(self):
        super().__init__(
            command_prefix=BOT_PREFIX,
            intents=get_bot_intents(),
            help_command=None  # We'll create a custom help command
        )
        self.music_players = {}  # Dictionary to store music players per guild
    
    async def setup_hook(self):
        """Load all cogs when the bot starts."""
        await self.load_cogs()
    
    async def load_cogs(self):
        """Dynamically load all cogs from the cogs directory."""
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('__'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f'✓ Loaded cog: {filename[:-3]}')
                except Exception as e:
                    print(f'✗ Failed to load cog {filename[:-3]}: {e}')
    
    async def on_ready(self):
        """Event handler for when the bot is ready."""
        print(f'\n{"="*50}')
        print(f'Bot is ready!')
        print(f'Logged in as: {self.user.name} (ID: {self.user.id})')
        print(f'Connected to {len(self.guilds)} guild(s)')
        print(f'Command prefix: {BOT_PREFIX}')
        print(f'{"="*50}\n')
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=f"{BOT_PREFIX}help | Music"
            )
        )
    
    async def on_command_error(self, ctx, error):
        """Global error handler for commands."""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"❌ Command not found. Use `{BOT_PREFIX}help` to see available commands.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Missing required argument: `{error.param.name}`")
        elif isinstance(error, commands.CheckFailure):
            # Check failures are handled in the checks themselves
            pass
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏰ This command is on cooldown. Try again in {error.retry_after:.1f}s")
        else:
            print(f'Error in command {ctx.command}: {error}')
            await ctx.send(f"❌ An error occurred: {str(error)}")
    
    async def on_voice_state_update(self, member, before, after):
        """Handle voice state updates (e.g., bot being alone in channel)."""
        if member.id == self.user.id:
            return
        
        # Check if bot is alone in voice channel
        if before.channel and self.user in before.channel.members:
            if len(before.channel.members) == 1:  # Only bot left
                voice_client = discord.utils.get(self.voice_clients, guild=member.guild)
                if voice_client:
                    # Stop playing and disconnect after 3 minutes of being alone
                    await asyncio.sleep(180)
                    if voice_client.channel and len(voice_client.channel.members) == 1:
                        await voice_client.disconnect()
                        if member.guild.id in self.music_players:
                            del self.music_players[member.guild.id]


def create_bot():
    """Create and return the bot instance."""
    if not DISCORD_TOKEN:
        raise ValueError("DISCORD_TOKEN not found in environment variables. Please check your .env file.")
    
    return MusicBot()

