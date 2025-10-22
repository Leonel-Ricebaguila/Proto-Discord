"""General utility commands for the Discord bot."""
import discord
from discord.ext import commands
from utils.config import BOT_PREFIX


class General(commands.Cog):
    """General commands cog with utility functions."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='ping')
    async def ping(self, ctx):
        """Check the bot's latency."""
        latency = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: `{latency}ms`",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='help')
    async def help(self, ctx, command_name: str = None):
        """Display help information for commands."""
        if command_name:
            # Show help for specific command
            command = self.bot.get_command(command_name)
            if command:
                embed = discord.Embed(
                    title=f"Help: {BOT_PREFIX}{command.name}",
                    description=command.help or "No description available.",
                    color=discord.Color.blue()
                )
                embed.add_field(
                    name="Usage",
                    value=f"`{BOT_PREFIX}{command.name} {command.signature}`",
                    inline=False
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Command `{command_name}` not found.")
        else:
            # Show general help
            embed = discord.Embed(
                title="🎵 Discord Music Bot - Help",
                description=f"Use `{BOT_PREFIX}help <command>` for more info on a command.",
                color=discord.Color.blue()
            )
            
            # Music commands
            music_commands = [
                f"`{BOT_PREFIX}play <url/query>` - Play music from URL or search",
                f"`{BOT_PREFIX}pause` - Pause the current track",
                f"`{BOT_PREFIX}resume` - Resume playback",
                f"`{BOT_PREFIX}skip` - Skip to the next track",
                f"`{BOT_PREFIX}stop` - Stop playback and clear queue",
                f"`{BOT_PREFIX}queue` - Display the current queue",
                f"`{BOT_PREFIX}nowplaying` - Show the current track",
                f"`{BOT_PREFIX}clear` - Clear the queue",
                f"`{BOT_PREFIX}leave` - Disconnect the bot from voice",
                f"`{BOT_PREFIX}volume [0-100]` - Set or show volume",
                f"`{BOT_PREFIX}equalizer [preset]` - Set audio equalizer (bass, treble, etc.)",
                f"`{BOT_PREFIX}filters` - Show current audio settings",
            ]
            embed.add_field(
                name="🎵 Music Commands",
                value="\n".join(music_commands),
                inline=False
            )
            
            # General commands
            general_commands = [
                f"`{BOT_PREFIX}ping` - Check bot latency",
                f"`{BOT_PREFIX}help` - Show this help message",
            ]
            embed.add_field(
                name="⚙️ General Commands",
                value="\n".join(general_commands),
                inline=False
            )
            
            embed.set_footer(text="Supports SoundCloud, YouTube, and more!")
            await ctx.send(embed=embed)
    
    @commands.command(name='invite')
    async def invite(self, ctx):
        """Get the bot invite link."""
        embed = discord.Embed(
            title="Invite Me!",
            description="Click the link below to add me to your server!",
            color=discord.Color.green()
        )
        
        # Generate invite URL
        permissions = discord.Permissions(
            connect=True,
            speak=True,
            send_messages=True,
            embed_links=True,
            read_message_history=True,
        )
        invite_url = discord.utils.oauth_url(
            self.bot.user.id,
            permissions=permissions
        )
        
        embed.add_field(name="Invite Link", value=f"[Click Here]({invite_url})", inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name='about')
    async def about(self, ctx):
        """Display information about the bot."""
        embed = discord.Embed(
            title="🎵 About This Bot",
            description="A Discord music bot with SoundCloud support!",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Servers", value=str(len(self.bot.guilds)), inline=True)
        embed.add_field(name="Prefix", value=BOT_PREFIX, inline=True)
        embed.add_field(
            name="Features",
            value="• Play music from SoundCloud & YouTube\n• Queue management\n• Basic playback controls",
            inline=False
        )
        
        await ctx.send(embed=embed)


async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(General(bot))



