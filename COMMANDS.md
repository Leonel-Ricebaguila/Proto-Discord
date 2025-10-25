# 🎵 Bot Commands Reference

Quick reference for all available commands.

## 🎵 Music Commands

| Command | Aliases | Usage | Description |
|---------|---------|-------|-------------|
| `!play` | `!p` | `!play <url or query>` | Play music or add to queue |
| `!pause` | - | `!pause` | Pause current playback |
| `!resume` | - | `!resume` | Resume paused playback |
| `!skip` | `!s` | `!skip` | Skip current track |
| `!stop` | - | `!stop` | Stop playback and clear queue |
| `!queue` | `!q` | `!queue` | Show current queue |
| `!nowplaying` | `!np` | `!nowplaying` | Show current track |
| `!clear` | - | `!clear` | Clear the queue |
| `!leave` | `!disconnect`, `!dc` | `!leave` | Disconnect from voice |
| `!volume` | `!vol` | `!volume [0-100]` | Set or show volume |

## ⚙️ General Commands

| Command | Usage | Description |
|---------|-------|-------------|
| `!help` | `!help [command]` | Show help message |
| `!ping` | `!ping` | Check bot latency |
| `!about` | `!about` | Show bot information |
| `!invite` | `!invite` | Get bot invite link |

## 📝 Usage Examples

### Playing Music

```bash
# Play from URL
!play https://soundcloud.com/artist/track
!play https://youtube.com/watch?v=xxxxx

# Search and play
!play lofi hip hop
!play never gonna give you up
!p relaxing music
```

### Queue Management

```bash
# View queue
!queue
!q

# Clear queue (keeps current song)
!clear

# Skip to next
!skip
!s

# Stop everything
!stop
```

### Playback Control

```bash
# Pause/Resume
!pause
!resume

# Volume control
!volume          # Show current volume
!volume 50       # Set to 50%
!vol 100         # Set to 100%

# Check what's playing
!nowplaying
!np
```

### Bot Control

```bash
# Disconnect bot
!leave
!disconnect
!dc

# Bot info
!ping            # Check latency
!about           # Bot information
!invite          # Get invite link
```

## 🎯 Tips

1. **You must be in a voice channel** to use music commands
2. **URLs supported**: SoundCloud, YouTube, Bandcamp, Twitch, and 1000+ sites
3. **Search queries** work for YouTube by default
4. **Volume** ranges from 0 (mute) to 100 (max)
5. **Queue** shows up to 10 upcoming tracks
6. **Embeds** display rich information with thumbnails

## 🚀 Quick Start

```bash
# 1. Join a voice channel
# 2. Play some music
!play https://soundcloud.com/track

# 3. Add more to queue
!play another song
!play yet another

# 4. Manage playback
!queue          # See what's queued
!skip           # Don't like this one
!pause          # Take a break
!resume         # Continue

# 5. Clean up
!clear          # Clear upcoming tracks
!stop           # Stop everything
!leave          # Disconnect bot
```

## ⚡ Keyboard Shortcuts

When typing commands, use these shortcuts:

- `!p` instead of `!play`
- `!s` instead of `!skip`
- `!q` instead of `!queue`
- `!np` instead of `!nowplaying`
- `!dc` instead of `!leave`

## 🎨 Command Features

- ✅ Beautiful embeds with track info
- ✅ Thumbnail images
- ✅ Duration display
- ✅ Requester information
- ✅ Real-time status updates
- ✅ Error messages with suggestions
- ✅ Auto-disconnect when alone

## 🔍 More Help

For detailed setup and troubleshooting:
- See **README.md** for full documentation
- See **QUICKSTART.md** for setup guide
- Use `!help <command>` for specific command help



