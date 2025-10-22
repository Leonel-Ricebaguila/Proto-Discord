# 🚀 Quick Start Guide

## For First-Time Users

### Step 1: Create Your Discord Bot (5 minutes)

1. Go to https://discord.com/developers/applications
2. Click **"New Application"**
3. Give it a name (e.g., "My Music Bot")
4. Go to **"Bot"** section → Click **"Add Bot"**
5. Under "Privileged Gateway Intents", enable:
   - ✅ **MESSAGE CONTENT INTENT** (Required!)
   - ✅ **PRESENCE INTENT** (Optional)
   - ✅ **SERVER MEMBERS INTENT** (Optional)
6. Click **"Reset Token"** and copy your bot token
   - ⚠️ **Keep this secret! Never share it!**

### Step 2: Install FFmpeg

**Windows:**
```powershell
# Using Chocolatey (recommended)
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update && sudo apt install ffmpeg
```

### Step 3: Setup the Bot

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Create `.env` file in the project root:**
```
DISCORD_TOKEN=paste_your_token_here
```

### Step 4: Invite Bot to Your Server

1. In Developer Portal, go to **"OAuth2"** → **"URL Generator"**
2. Select scopes:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Select permissions:
   - ✅ Connect
   - ✅ Speak  
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Read Message History
4. Copy the URL at the bottom and open it
5. Select your server and click **"Authorize"**

### Step 5: Run the Bot

```bash
python main.py
```

✅ If you see "Bot is ready!" - you're all set!

### Step 6: Test It Out

1. Join a voice channel in your Discord server
2. Type in any text channel:
```
!play https://soundcloud.com/artist/song
```

or search for a song:
```
!play lofi hip hop
```

## Common Issues

### "FFmpeg not found"
- Make sure FFmpeg is installed
- Restart your terminal after installation
- On Windows, you may need to add FFmpeg to PATH

### Bot doesn't respond
- Check MESSAGE CONTENT INTENT is enabled
- Verify the bot has proper permissions
- Check the bot is online (green dot)

### "Failed to load track"
- Update yt-dlp: `pip install --upgrade yt-dlp`
- Try a different URL
- Check your internet connection

## Example Commands

```bash
# Play music
!play https://soundcloud.com/track
!play never gonna give you up

# Queue management  
!queue          # Show current queue
!skip           # Skip current song
!clear          # Clear the queue

# Playback controls
!pause          # Pause playback
!resume         # Resume playback
!stop           # Stop and disconnect
!volume 50      # Set volume to 50%

# Information
!nowplaying     # Show current song
!help           # Show all commands
```

## Supported Platforms

- ✅ SoundCloud
- ✅ YouTube
- ✅ YouTube Music
- ✅ Bandcamp
- ✅ Twitch
- ✅ And 1000+ more!

## Next Steps

Once your bot is working locally:

1. **Deploy to Cloud:** See README.md for Railway, Render, or Fly.io setup
2. **Customize:** Edit `utils/config.py` to change prefix, settings, etc.
3. **Add Features:** Check `cogs/` folder to add new commands

## Need Help?

Check the full [README.md](README.md) for detailed documentation!




