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
}

# FFmpeg options for audio streaming (base)
FFMPEG_BASE_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin',
    'options': '-vn -b:a 128k',
}

# Equalizer presets using FFmpeg audio filters
EQUALIZER_PRESETS = {
    'flat': {
        'name': 'Flat (No EQ)',
        'description': 'No equalization, natural sound',
        'filter': None,  # No filter
    },
    'bass': {
        'name': 'Bass Boost',
        'description': 'Enhanced low frequencies for deeper sound (3-band: 60Hz, 110Hz, 250Hz)',
        'filter': 'bass=g=1:f=60:w=0.2,bass=g=2:f=110:w=0.3,bass=g=3:f=250:w=0.2',
    },
    'treble': {
        'name': 'Treble Boost',
        'description': 'Enhanced high frequencies for clearer sound',
        'filter': 'treble=g=8:f=5000:w=0.5',  # Boost treble at 5kHz
    },
    'nightcore': {
        'name': 'Nightcore',
        'description': 'Higher pitch and faster tempo',
        'filter': 'asetrate=48000*1.15,atempo=1.15',
    },
    'vaporwave': {
        'name': 'Vaporwave',
        'description': 'Slower and lower pitch',
        'filter': 'asetrate=48000*0.85,atempo=0.85',
    },
    'soft': {
        'name': 'Soft',
        'description': 'Gentle, reduced harsh frequencies',
        'filter': 'equalizer=f=1000:t=h:width=200:g=-2,equalizer=f=5000:t=h:width=1000:g=-4',
    },
    'party': {
        'name': 'Party Mode',
        'description': 'Boosted bass and treble for energetic sound',
        'filter': 'bass=g=8:f=110:w=0.3,treble=g=5:f=5000:w=0.5',
    },
    'clear': {
        'name': 'Clear Voice',
        'description': 'Optimized for voice clarity',
        'filter': 'equalizer=f=3000:t=h:width=1000:g=5,highpass=f=100',
    },
}

def get_ffmpeg_options(equalizer='flat'):
    """
    Get FFmpeg options with the specified equalizer preset.
    
    Args:
        equalizer: Name of the equalizer preset (default: 'flat')
    
    Returns:
        Dictionary of FFmpeg options
    """
    options = FFMPEG_BASE_OPTIONS.copy()
    
    if equalizer in EQUALIZER_PRESETS and EQUALIZER_PRESETS[equalizer]['filter']:
        # Add audio filter to options
        filter_str = EQUALIZER_PRESETS[equalizer]['filter']
        options['options'] = f"{options['options']} -af {filter_str}"
    
    return options

# Legacy support - default options without filter
FFMPEG_OPTIONS = FFMPEG_BASE_OPTIONS.copy()

# Bot intents configuration
def get_bot_intents():
    """Get the required Discord bot intents."""
    import discord
    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True
    intents.guilds = True
    return intents


