# 🎵 Discord SoundCloud Music Bot

A feature-rich Discord music bot built with Python that supports SoundCloud, YouTube, and many other platforms. Built with a modular cog-based architecture for easy maintenance and extensibility.

## ✨ Features

- 🎵 Play music from SoundCloud, YouTube, and 1000+ other sites
- 📋 Queue management with playlist support
- ⏯️ Full playback controls (play, pause, resume, skip, stop)
- 🔊 Volume control
- 📱 Beautiful embed messages with track information
- 🎯 Easy-to-use commands with aliases
- 🔧 Modular cog-based architecture
- 🌐 Free cloud hosting support (Railway, Render, Fly.io)

## 📋 Commands

### Music Commands

| Command | Aliases | Description |
|---------|---------|-------------|
| `!play <url/query>` | `!p` | Play music from URL or search query |
| `!pause` | - | Pause the current track |
| `!resume` | - | Resume playback |
| `!skip` | `!s` | Skip to the next track |
| `!stop` | - | Stop playback and clear queue |
| `!queue` | `!q` | Display the current queue |
| `!nowplaying` | `!np` | Show currently playing track |
| `!clear` | - | Clear the queue |
| `!leave` | `!disconnect`, `!dc` | Disconnect from voice channel |
| `!volume <0-100>` | `!vol` | Set or display volume |

### General Commands

| Command | Description |
|---------|-------------|
| `!help [command]` | Show help message or command info |
| `!ping` | Check bot latency |
| `!about` | Show bot information |
| `!invite` | Get bot invite link |

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- FFmpeg (required for audio processing)
- Discord Bot Token

### 1. Install FFmpeg

**Windows:**
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract and add to PATH
3. Or use Chocolatey: `choco install ffmpeg`

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

### 2. Clone the Repository

```bash
git clone <your-repo-url>
cd proto_discord_bot
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. **Important:** Enable these intents under "Privileged Gateway Intents":
   - ✅ MESSAGE CONTENT INTENT
   - ✅ SERVER MEMBERS INTENT (optional)
5. Copy the bot token (you'll need this for the next step)

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```bash
DISCORD_TOKEN=your_discord_bot_token_here
```

**Never share or commit your bot token!**

### 6. Invite Bot to Your Server

1. In the Developer Portal, go to "OAuth2" → "URL Generator"
2. Select scopes:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Select bot permissions:
   - ✅ Connect
   - ✅ Speak
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Read Message History
   - ✅ Use Voice Activity
4. Copy the generated URL and open it in your browser
5. Select your server and authorize the bot

### 7. Run the Bot

```bash
python main.py
```

You should see:
```
✓ Loaded cog: general
✓ Loaded cog: music

==================================================
Bot is ready!
Logged in as: YourBotName (ID: 123456789)
Connected to 1 guild(s)
Command prefix: !
==================================================
```

## 🌐 Cloud Deployment

Deploy your bot to run 24/7 on free cloud hosting platforms.

### Option 1: Railway (Recommended)

**Free Tier:** 500 hours/month

1. Create account at [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add environment variable: `DISCORD_TOKEN=your_token`
5. Railway will automatically detect Python and deploy

**Manual deployment:**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and initialize
railway login
railway init

# Deploy
railway up
```

### Option 2: Render.com

**Free Tier:** 750 hours/month

1. Create account at [render.com](https://render.com)
2. Click "New +" → "Background Worker"
3. Connect your GitHub repository
4. Configure:
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`
5. Add environment variable: `DISCORD_TOKEN=your_token`
6. Click "Create Background Worker"

### Option 3: Fly.io

**Free Tier:** Generous free tier with credits

1. Install Fly CLI:
```bash
# macOS/Linux
curl -L https://fly.io/install.sh | sh

# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

2. Login and launch:
```bash
fly auth login
fly launch
```

3. Follow the prompts and deploy:
```bash
fly deploy
```

4. Set environment variable:
```bash
fly secrets set DISCORD_TOKEN=your_token
```

## 📁 Project Structure

```
proto_discord_bot/
├── main.py                 # Entry point
├── bot.py                  # Bot initialization & cog loader
├── cogs/                   # Command modules
│   ├── __init__.py
│   ├── music.py           # Music commands
│   └── general.py         # General commands
├── utils/                  # Utility modules
│   ├── __init__.py
│   ├── config.py          # Configuration
│   ├── music_player.py    # Music player logic
│   └── checks.py          # Custom checks
├── requirements.txt        # Python dependencies
├── Procfile               # Railway/Render config
├── railway.toml           # Railway config
├── render.yaml            # Render config
├── .env                   # Environment variables (create this)
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following:

```env
DISCORD_TOKEN=your_discord_bot_token_here
```

### Bot Prefix

To change the command prefix, edit `utils/config.py`:

```python
BOT_PREFIX = '!'  # Change to your preferred prefix
```

### Audio Quality

Adjust audio quality settings in `utils/config.py`:

```python
YTDL_OPTIONS = {
    'format': 'bestaudio/best',  # Best available quality
    # ... other options
}
```

## 🎵 Supported Platforms

Thanks to yt-dlp, the bot supports music from:

- SoundCloud
- YouTube (videos & playlists)
- Spotify (track info only)
- Bandcamp
- Twitch
- And 1000+ more sites!

**Note:** No SoundCloud API key required - yt-dlp handles everything automatically!

## 🐛 Troubleshooting

### Bot doesn't respond to commands

1. Check that MESSAGE CONTENT INTENT is enabled in Discord Developer Portal
2. Verify the bot has proper permissions in your server
3. Make sure you're using the correct command prefix (`!` by default)

### "FFmpeg not found" error

Install FFmpeg and ensure it's in your system PATH:
- Windows: Add FFmpeg to Environment Variables
- macOS/Linux: Install via package manager

### Bot disconnects after playing one song

This is usually a network issue. Try:
1. Restarting the bot
2. Checking your internet connection
3. Using a different hosting platform

### "Failed to load track" error

1. Check if the URL is valid and accessible
2. Try updating yt-dlp: `pip install --upgrade yt-dlp`
3. Some content may be region-restricted or require authentication

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is open source and available for personal use.

## ⚠️ Disclaimer

This bot is for educational purposes. Make sure to comply with:
- Discord's Terms of Service
- Discord's Bot Guidelines
- Copyright laws in your jurisdiction
- Terms of service of the platforms you're streaming from

## 💬 Support

If you encounter issues:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the Discord bot logs for error messages
3. Ensure all dependencies are installed correctly
4. Verify FFmpeg is properly installed

## 🎉 Credits

Built with:
- [discord.py](https://github.com/Rapptz/discord.py) - Discord API wrapper
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Media extraction tool
- Python 3.8+

---

Made with ❤️ for Discord music lovers




