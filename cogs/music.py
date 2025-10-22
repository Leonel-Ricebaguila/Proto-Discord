"""Music commands cog for the Discord bot."""
import discord
from discord.ext import commands
from utils.music_player import MusicPlayer
from utils.checks import is_in_voice_channel, is_in_same_voice_channel
from utils.config import EQUALIZER_PRESETS


class Music(commands.Cog):
    """Music commands cog with playback controls."""
    
    def __init__(self, bot):
        self.bot = bot
    
    def get_player(self, ctx) -> MusicPlayer:
        """Get or create a music player for the guild."""
        if ctx.guild.id not in self.bot.music_players:
            self.bot.music_players[ctx.guild.id] = MusicPlayer(ctx)
        return self.bot.music_players[ctx.guild.id]
    
    @commands.command(name='play', aliases=['p'])
    @is_in_voice_channel()
    async def play(self, ctx, *, query: str):
        """Play music from a URL or search query.
        
        Supports SoundCloud, YouTube, and many other platforms.
        You can provide a direct URL or a search query.
        """
        # Connect to voice channel if not already connected
        if not ctx.voice_client:
            try:
                await ctx.author.voice.channel.connect()
            except Exception as e:
                await ctx.send(f"❌ Failed to connect to voice channel: {str(e)}")
                return
        elif ctx.voice_client.channel != ctx.author.voice.channel:
            await ctx.voice_client.move_to(ctx.author.voice.channel)
        
        # Get the music player for this guild
        player = self.get_player(ctx)
        player.voice_client = ctx.voice_client
        player.ctx = ctx
        
        # Send loading message
        loading_msg = await ctx.send("🔍 Searching and loading track...")
        
        # Add track(s) to queue
        result = await player.add_track(query, ctx.author)
        
        if result:
            # Delete loading message
            await loading_msg.delete()
            
            tracks = result['tracks']
            is_playlist = result['is_playlist']
            
            # If not currently playing, start playback
            if not player.is_playing and not ctx.voice_client.is_playing():
                await player.play_next()
            
            # Send appropriate message
            if is_playlist:
                # Playlist - show all tracks in one message
                embed = discord.Embed(
                    title="📋 Playlist Added to Queue",
                    description=f"**{result['playlist_name']}**\n{len(tracks)} track(s) added",
                    color=discord.Color.green()
                )
                
                # Show up to 10 tracks
                track_list = []
                for i, track in enumerate(tracks[:10], 1):
                    duration = track.format_duration()
                    track_list.append(f"`{i}.` {track.title} `[{duration}]`")
                
                embed.add_field(
                    name="Tracks",
                    value="\n".join(track_list),
                    inline=False
                )
                
                if len(tracks) > 10:
                    embed.add_field(
                        name="And more...",
                        value=f"+{len(tracks) - 10} additional track(s)",
                        inline=False
                    )
                
                embed.add_field(name="Requested by", value=ctx.author.mention, inline=True)
                embed.add_field(name="Total in queue", value=str(len(player.queue)), inline=True)
                
                if tracks[0].thumbnail:
                    embed.set_thumbnail(url=tracks[0].thumbnail)
                
                embed.set_footer(text="Use !queue to see the full queue")
                await ctx.send(embed=embed)
            else:
                # Single track
                track = tracks[0]
                if player.is_playing or ctx.voice_client.is_playing():
                    # Show queued message
                    embed = discord.Embed(
                        title="✅ Added to Queue",
                        description=f"[{track.title}]({track.webpage_url})" if track.webpage_url.startswith('http') else track.title,
                        color=discord.Color.blue()
                    )
                    embed.add_field(name="Duration", value=track.format_duration(), inline=True)
                    embed.add_field(name="Position in queue", value=str(len(player.queue)), inline=True)
                    embed.add_field(name="Requested by", value=ctx.author.mention, inline=True)
                    if track.thumbnail:
                        embed.set_thumbnail(url=track.thumbnail)
                    await ctx.send(embed=embed)
        else:
            await loading_msg.edit(content="❌ Failed to load track. Please check the URL or try a different search query.")
    
    @commands.command(name='pause')
    @is_in_same_voice_channel()
    async def pause(self, ctx):
        """Pause the current track."""
        player = self.get_player(ctx)
        
        if player.pause():
            await ctx.send("⏸️ Paused playback.")
        else:
            await ctx.send("❌ Nothing is currently playing.")
    
    @commands.command(name='resume')
    @is_in_same_voice_channel()
    async def resume(self, ctx):
        """Resume the paused track."""
        player = self.get_player(ctx)
        
        if player.resume():
            await ctx.send("▶️ Resumed playback.")
        else:
            await ctx.send("❌ Nothing is currently paused.")
    
    @commands.command(name='skip', aliases=['s'])
    @is_in_same_voice_channel()
    async def skip(self, ctx):
        """Skip the current track."""
        player = self.get_player(ctx)
        
        if player.skip():
            await ctx.send("⏭️ Skipped to the next track.")
        else:
            await ctx.send("❌ Nothing is currently playing.")
    
    @commands.command(name='stop')
    @is_in_same_voice_channel()
    async def stop(self, ctx):
        """Stop playback and clear the queue."""
        player = self.get_player(ctx)
        player.stop()
        
        await ctx.send("⏹️ Stopped playback and cleared the queue.")
    
    @commands.command(name='queue', aliases=['q'])
    async def queue(self, ctx):
        """Display the current queue."""
        player = self.get_player(ctx)
        
        if not player.current and len(player.queue) == 0:
            await ctx.send("📭 The queue is empty. Use `!play` to add music!")
            return
        
        embed = discord.Embed(
            title="🎵 Music Queue",
            color=discord.Color.blue()
        )
        
        # Show currently playing
        if player.current:
            embed.add_field(
                name="🎵 Now Playing",
                value=f"[{player.current.title}]({player.current.webpage_url})\n"
                      f"Duration: {player.current.format_duration()} | "
                      f"Requested by: {player.current.requester.mention}",
                inline=False
            )
        
        # Show upcoming tracks
        if len(player.queue) > 0:
            queue_text = []
            for i, track in enumerate(player.queue[:10], 1):  # Show first 10 tracks
                queue_text.append(
                    f"`{i}.` [{track.title}]({track.webpage_url}) "
                    f"[{track.format_duration()}]"
                )
            
            embed.add_field(
                name=f"📋 Up Next ({len(player.queue)} tracks)",
                value="\n".join(queue_text),
                inline=False
            )
            
            if len(player.queue) > 10:
                embed.set_footer(text=f"And {len(player.queue) - 10} more...")
        
        await ctx.send(embed=embed)
    
    @commands.command(name='nowplaying', aliases=['np'])
    async def nowplaying(self, ctx):
        """Display the currently playing track."""
        player = self.get_player(ctx)
        
        if not player.current:
            await ctx.send("❌ Nothing is currently playing.")
            return
        
        embed = discord.Embed(
            title="🎵 Now Playing",
            description=f"[{player.current.title}]({player.current.webpage_url})",
            color=discord.Color.green()
        )
        
        embed.add_field(name="Duration", value=player.current.format_duration(), inline=True)
        embed.add_field(name="Requested by", value=player.current.requester.mention, inline=True)
        
        if player.current.thumbnail:
            embed.set_thumbnail(url=player.current.thumbnail)
        
        # Show queue length
        if len(player.queue) > 0:
            embed.add_field(
                name="Up Next",
                value=f"{len(player.queue)} track(s) in queue",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='clear')
    @is_in_same_voice_channel()
    async def clear(self, ctx):
        """Clear the queue without stopping the current track."""
        player = self.get_player(ctx)
        
        if len(player.queue) == 0:
            await ctx.send("❌ The queue is already empty.")
            return
        
        queue_length = len(player.queue)
        player.clear_queue()
        await ctx.send(f"🗑️ Cleared {queue_length} track(s) from the queue.")
    
    @commands.command(name='leave', aliases=['disconnect', 'dc'])
    @is_in_same_voice_channel()
    async def leave(self, ctx):
        """Disconnect the bot from the voice channel."""
        if ctx.voice_client:
            player = self.get_player(ctx)
            player.stop()
            
            await ctx.voice_client.disconnect()
            await ctx.send("👋 Disconnected from voice channel.")
            
            # Remove player from dictionary
            if ctx.guild.id in self.bot.music_players:
                del self.bot.music_players[ctx.guild.id]
        else:
            await ctx.send("❌ The bot is not connected to a voice channel.")
    
    @commands.command(name='volume', aliases=['vol'])
    @is_in_same_voice_channel()
    async def volume(self, ctx, volume: int = None):
        """Set or display the playback volume (0-100)."""
        if ctx.voice_client is None:
            await ctx.send("❌ The bot is not connected to a voice channel.")
            return
        
        if volume is None:
            # Display current volume
            if ctx.voice_client.source:
                current_volume = int(ctx.voice_client.source.volume * 100)
                await ctx.send(f"🔊 Current volume: {current_volume}%")
            else:
                await ctx.send("❌ Nothing is currently playing.")
            return
        
        # Set volume
        if not 0 <= volume <= 100:
            await ctx.send("❌ Volume must be between 0 and 100.")
            return
        
        if ctx.voice_client.source:
            ctx.voice_client.source.volume = volume / 100
            await ctx.send(f"🔊 Volume set to {volume}%")
        else:
            await ctx.send("❌ Nothing is currently playing.")
    
    @commands.command(name='equalizer', aliases=['eq'])
    async def equalizer(self, ctx, preset: str = None):
        """Set or display the audio equalizer preset.
        
        Available presets:
        - flat: No equalization (default)
        - bass: Bass boost
        - treble: Treble boost
        - nightcore: Higher pitch and faster
        - vaporwave: Lower pitch and slower
        - soft: Gentle, reduced harsh frequencies
        - party: Boosted bass and treble
        - clear: Optimized for voice clarity
        """
        player = self.get_player(ctx)
        
        if preset is None:
            # Display current equalizer and available presets
            embed = discord.Embed(
                title="🎛️ Audio Equalizer",
                description=f"Current preset: **{EQUALIZER_PRESETS[player.equalizer]['name']}**",
                color=discord.Color.purple()
            )
            
            # List all available presets
            presets_text = []
            for key, value in EQUALIZER_PRESETS.items():
                marker = "🔊" if key == player.equalizer else "⚪"
                presets_text.append(f"{marker} **{key}** - {value['name']}\n   _{value['description']}_")
            
            embed.add_field(
                name="Available Presets",
                value="\n\n".join(presets_text),
                inline=False
            )
            
            embed.set_footer(text=f"Use {ctx.prefix}eq <preset> to change | Changes apply to next track")
            await ctx.send(embed=embed)
            return
        
        # Set new equalizer preset
        preset = preset.lower()
        if preset not in EQUALIZER_PRESETS:
            await ctx.send(
                f"❌ Invalid preset! Use `{ctx.prefix}eq` to see available presets."
            )
            return
        
        player.equalizer = preset
        preset_info = EQUALIZER_PRESETS[preset]
        
        embed = discord.Embed(
            title="🎛️ Equalizer Updated",
            description=f"Set to: **{preset_info['name']}**\n_{preset_info['description']}_",
            color=discord.Color.green()
        )
        
        # Note about when it applies
        if player.is_playing:
            embed.add_field(
                name="📝 Note",
                value="The new equalizer will apply to the next track.\nUse `!skip` to apply it to a new song now.",
                inline=False
            )
        else:
            embed.add_field(
                name="✅ Ready",
                value="The equalizer will be applied to all upcoming tracks.",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='filters')
    async def filters(self, ctx):
        """Show current audio filters and equalizer settings."""
        player = self.get_player(ctx)
        
        embed = discord.Embed(
            title="🎚️ Current Audio Settings",
            color=discord.Color.blue()
        )
        
        # Equalizer info
        preset_info = EQUALIZER_PRESETS[player.equalizer]
        embed.add_field(
            name="🎛️ Equalizer",
            value=f"**{preset_info['name']}**\n{preset_info['description']}",
            inline=False
        )
        
        # Volume info
        if ctx.voice_client and ctx.voice_client.source:
            current_volume = int(ctx.voice_client.source.volume * 100)
            embed.add_field(
                name="🔊 Volume",
                value=f"{current_volume}%",
                inline=True
            )
        
        # Playing status
        if player.is_playing:
            embed.add_field(
                name="▶️ Status",
                value="Playing",
                inline=True
            )
        
        embed.set_footer(text=f"Use {ctx.prefix}eq to change equalizer | {ctx.prefix}volume to adjust volume")
        await ctx.send(embed=embed)


async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(Music(bot))



