"""Configuration management for the Discord music bot."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = '!'

# yt-dlp configuration for audio extraction
YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,  # Allow playlists
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',  # Default to YouTube search
    'source_address': '0.0.0.0',
    # YouTube bot detection bypass
    'extractor_args': {
        'youtube': {
            'player_client': ['android', 'web'],
            'player_skip': ['webpage', 'configs'],
        }
    },
    # Additional options to avoid bot detection
    'nocache': True,
    'age_limit': None,
}

# FFmpeg options for audio streaming
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin',
    'options': '-vn -b:a 128k',
}

# Bot intents configuration
def get_bot_intents():
    """Get the required Discord bot intents."""
    import discord
    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True
    intents.guilds = True
    return intents


