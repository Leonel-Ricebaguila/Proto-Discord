"""Music player logic and queue management."""
import asyncio
import discord
import yt_dlp as youtube_dl
from typing import Optional, List
from utils.config import YTDL_OPTIONS, FFMPEG_OPTIONS


class Track:
    """Represents a music track."""
    
    def __init__(self, title: str, url: str, webpage_url: str, duration: int, 
                 thumbnail: Optional[str] = None, requester: Optional[discord.Member] = None):
        self.title = title
        self.url = url
        self.webpage_url = webpage_url
        self.duration = duration
        self.thumbnail = thumbnail
        self.requester = requester
    
    def format_duration(self) -> str:
        """Format duration in MM:SS or HH:MM:SS format."""
        if self.duration:
            hours, remainder = divmod(self.duration, 3600)
            minutes, seconds = divmod(remainder, 60)
            if hours > 0:
                return f"{int(hours)}:{int(minutes):02d}:{int(seconds):02d}"
            return f"{int(minutes)}:{int(seconds):02d}"
        return "Unknown"


class MusicPlayer:
    """Manages the music queue and playback for a guild."""
    
    def __init__(self, ctx):
        self.ctx = ctx
        self.queue: List[Track] = []
        self.current: Optional[Track] = None
        self.voice_client: Optional[discord.VoiceClient] = None
        self.ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)
        self.is_playing = False
        self.loop = False
    
    async def add_track(self, query: str, requester: discord.Member):
        """Extract track information and add to queue.
        
        Returns:
            dict: {'tracks': [Track], 'is_playlist': bool, 'playlist_name': str or None}
            or None if failed
        """
        try:
            # Run yt-dlp in executor to avoid blocking
            print(f"Fetching info for: {query}")
            data = await asyncio.to_thread(self._extract_info, query)
            
            if data is None:
                return None
            
            # Handle playlists/search results
            if 'entries' in data:
                # Get first entry for single track or first in playlist
                if data['entries']:
                    tracks_added = []
                    for entry in data['entries']:
                        if entry:
                            # Check if entry has minimal required data
                            # If not (like with flat extraction), we need the URL to re-extract
                            entry_url = entry.get('webpage_url') or entry.get('url') or entry.get('id')
                            entry_title = entry.get('title', 'Unknown Title')
                            
                            if not entry_url:
                                print(f"Skipping entry without URL: {entry_title}")
                                continue
                            
                            # If we don't have full info (title, duration, etc), extract it now
                            if entry_title == 'Unknown Title' or not entry.get('duration'):
                                print(f"Extracting full info for: {entry_url}")
                                try:
                                    full_data = await asyncio.to_thread(
                                        self.ytdl.extract_info, 
                                        entry_url, 
                                        download=False
                                    )
                                    if full_data:
                                        entry = full_data
                                except Exception as e:
                                    print(f"Failed to extract full info for {entry_url}: {e}")
                                    continue
                            
                            print(f"Adding track: {entry.get('title', 'Unknown')} | URL: {entry.get('webpage_url', 'N/A')}")
                            track = self._create_track(entry, requester)
                            self.queue.append(track)
                            tracks_added.append(track)
                    
                    if tracks_added:
                        return {
                            'tracks': tracks_added,
                            'is_playlist': len(tracks_added) > 1,
                            'playlist_name': data.get('title', 'Playlist')
                        }
                return None
            else:
                # Single track
                print(f"Adding track: {data.get('title', 'Unknown')} | URL: {data.get('webpage_url', 'N/A')}")
                track = self._create_track(data, requester)
                self.queue.append(track)
                return {
                    'tracks': [track],
                    'is_playlist': False,
                    'playlist_name': None
                }
                
        except Exception as e:
            print(f"Error adding track: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _extract_info(self, query: str):
        """Extract information using yt-dlp."""
        try:
            return self.ytdl.extract_info(query, download=False)
        except Exception as e:
            print(f"yt-dlp error: {e}")
            return None
    
    def _create_track(self, data: dict, requester: discord.Member) -> Track:
        """Create a Track object from yt-dlp data."""
        # Get the best available identifier for re-extraction
        webpage_url = data.get('webpage_url') or data.get('url') or data.get('id', '')
        
        return Track(
            title=data.get('title', 'Unknown Title'),
            url=data.get('url', ''),
            webpage_url=webpage_url,
            duration=data.get('duration', 0),
            thumbnail=data.get('thumbnail'),
            requester=requester
        )
    
    async def play_next(self):
        """Play the next track in the queue."""
        if len(self.queue) > 0:
            self.current = self.queue.pop(0)
            self.is_playing = True
            
            try:
                # Always re-extract fresh URL for reliability
                # (Cached URLs often expire or are webpage URLs, not audio streams)
                if not self.current.webpage_url or not self.current.webpage_url.startswith('http'):
                    raise Exception("Invalid webpage URL - cannot extract audio")
                
                print(f"Extracting fresh audio URL for: {self.current.webpage_url}")
                fresh_data = await asyncio.to_thread(
                    self.ytdl.extract_info, 
                    self.current.webpage_url, 
                    download=False
                )
                
                if fresh_data and 'url' in fresh_data:
                    audio_url = fresh_data['url']
                elif fresh_data and 'entries' in fresh_data and fresh_data['entries']:
                    audio_url = fresh_data['entries'][0]['url']
                else:
                    raise Exception("Could not extract audio URL")
                
                print(f"Playing audio from: {audio_url[:100]}...")
                
                # Create FFmpeg audio source with fresh URL
                source = discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS)
                source = discord.PCMVolumeTransformer(source, volume=0.5)
                
                # Play the audio
                self.voice_client.play(
                    source,
                    after=lambda e: asyncio.run_coroutine_threadsafe(
                        self._after_playing(e), self.ctx.bot.loop
                    )
                )
                
                # Send now playing message
                embed = discord.Embed(
                    title="🎵 Now Playing",
                    description=f"[{self.current.title}]({self.current.webpage_url})" if self.current.webpage_url.startswith('http') else self.current.title,
                    color=discord.Color.green()
                )
                embed.add_field(name="Duration", value=self.current.format_duration())
                embed.add_field(name="Requested by", value=self.current.requester.mention)
                if self.current.thumbnail:
                    embed.set_thumbnail(url=self.current.thumbnail)
                
                await self.ctx.send(embed=embed)
                
            except Exception as e:
                print(f"Error playing track: {e}")
                await self.ctx.send(f"❌ Error playing track: {str(e)}")
                self.is_playing = False
                await self.play_next()
        else:
            self.is_playing = False
            self.current = None
    
    async def _after_playing(self, error):
        """Callback after a track finishes playing."""
        if error:
            print(f"Player error: {error}")
        
        self.is_playing = False
        
        # If loop is enabled, re-add the current track
        if self.loop and self.current:
            self.queue.insert(0, self.current)
        
        # Play next track
        await self.play_next()
    
    def pause(self):
        """Pause the current playback."""
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.pause()
            return True
        return False
    
    def resume(self):
        """Resume the paused playback."""
        if self.voice_client and self.voice_client.is_paused():
            self.voice_client.resume()
            return True
        return False
    
    def skip(self):
        """Skip the current track."""
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()
            return True
        return False
    
    def stop(self):
        """Stop playback and clear the queue."""
        self.queue.clear()
        self.current = None
        self.is_playing = False
        if self.voice_client:
            self.voice_client.stop()
    
    def clear_queue(self):
        """Clear the queue without stopping current track."""
        self.queue.clear()
    
    def get_queue(self) -> List[Track]:
        """Get the current queue."""
        return self.queue.copy()


