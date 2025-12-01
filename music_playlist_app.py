"""
Music Playlist App
- Song info stored as a tuple: (name, artist, length_seconds)
- Uses OOP: base Song wrapper stores tuple, LocalSong and OnlineSong implement polymorphic play()
- Playlist class manages add/remove/shuffle/play and a Recently Played list (deque)
"""                                                                                                                                                                                                                                                                  

from typing import Tuple, List, Optional
from collections import deque
import random
import time

# ---------- Helper functions ----------

def format_length(seconds: int) -> str:
    """Convert seconds to 'MM:SS' string for display."""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"

# ---------- Song classes (OOP + polymorphism) ----------

class Song:
    """
    Generic Song container that stores song info in a tuple.
    The 'info' attribute is a tuple: (name, artist, length_seconds)
    """
    def __init__(self, name: str, artist: str, length_seconds: int):
        # store core song data as a tuple as requested
        self.info: Tuple[str, str, int] = (name, artist, length_seconds)

    @property
    def name(self) -> str:
        return self.info[0]

    @property
    def artist(self) -> str:
        return self.info[1]

    @property
    def length_seconds(self) -> int:
        return self.info[2]

    def __repr__(self) -> str:
        return f"{self.name} — {self.artist} ({format_length(self.length_seconds)})"

    # Polymorphic 'play' method — subclasses override this.
    def play(self) -> None:
        raise NotImplementedError("Subclasses must implement play()")


class LocalSong(Song):
    """
    LocalSong represents a song stored locally on disk.
    Polymorphic play(): simulates playing a local file.
    """
    def __init__(self, name: str, artist: str, length_seconds: int, file_path: Optional[str] = None):
        super().__init__(name, artist, length_seconds)
        # extra attribute local to LocalSong
        self.file_path = file_path or f"/music/{self.name}.mp3"

    def play(self) -> None:
        # In a real app we'd open the file; here we simulate playback with prints.
        print(f"[Local] Playing '{self.name}' by {self.artist} from file: {self.file_path}")
        # Simulate a short 'playing' time (not the full song length) so demo doesn't hang
        time.sleep(0.3)


class OnlineSong(Song):
    """
    OnlineSong represents a song streamed from a URL (e.g., YouTube, Spotify link).
    Polymorphic play(): simulates streaming playback.
    """
    def __init__(self, name: str, artist: str, length_seconds: int, stream_url: Optional[str] = None):
        super().__init__(name, artist, length_seconds)
        # extra attribute local to OnlineSong
        self.stream_url = stream_url or f"https://stream.example/{self.name.replace(' ', '_')}"

    def play(self) -> None:
        # Simulate streaming playback
        print(f"[Online] Streaming '{self.name}' by {self.artist} from: {self.stream_url}")
        # Simulate a short 'buffer/play' time
        time.sleep(0.4)


# ---------- Playlist manager ----------

class Playlist:
    """
    Playlist holds a list of Song objects and a Recently Played deque.
    Features:
    - add_song
    - remove_song (by name or index)
    - shuffle
    - play_song (calls song.play() polymorphically)
    - show playlist and recently played
    """
    def __init__(self, name: str = "My Playlist", recently_played_limit: int = 10):
        self.name = name
        self.songs: List[Song] = []  # ordered list of Song objects
        # deque to keep most recent plays; newest appended to the right
        self.recently_played: deque[Song] = deque(maxlen=recently_played_limit)

    def add_song(self, song: Song) -> None:
        """Add a Song object to the end of the playlist."""
        self.songs.append(song)
        print(f"Added: {song}")

    def remove_song_by_name(self, name: str) -> bool:
        """
        Remove the first song with matching name.
        Returns True if removed, False if not found.
        """
        for i, s in enumerate(self.songs):
            if s.name == name:
                removed = self.songs.pop(i)
                print(f"Removed: {removed}")
                return True
        print(f"Song named '{name}' not found in playlist.")
        return False

    def remove_song_by_index(self, index: int) -> bool:
        """
        Remove song at index (0-based). Returns True if successful, False if index invalid.
        """
        if 0 <= index < len(self.songs):
            removed = self.songs.pop(index)
            print(f"Removed at index {index}: {removed}")
            return True
        print(f"Index {index} out of range (0..{len(self.songs)-1}).")
        return False

    def shuffle(self) -> None:
        """Shuffle playlist in-place randomly."""
        if len(self.songs) <= 1:
            print("Not enough songs to shuffle.")
            return
        random.shuffle(self.songs)
        print("Playlist shuffled.")

    def play_song(self, index: int) -> None:
        """
        Play the song at the given index.
        Calls the song's play() method (polymorphism) and updates recently_played.
        """
        if not (0 <= index < len(self.songs)):
            print(f"Index {index} out of range. Cannot play.")
            return
        song = self.songs[index]
        # Polymorphic call: LocalSong.play() or OnlineSong.play()
        song.play()
        # Add to recently played (deque handles max length)
        self.recently_played.append(song)
        print(f"--> Added to Recently Played: {song}")

    def play_next(self) -> None:
        """
        Play the first song (like a queue 'next'), then remove it from playlist if desired.
        Here we just play and leave it in the playlist.
        """
        if not self.songs:
            print("Playlist is empty.")
            return
        self.play_song(0)

    def show(self) -> None:
        """Print the playlist with indices and song info."""
        print(f"--- {self.name} ({len(self.songs)} songs) ---")
        for i, s in enumerate(self.songs):
            print(f"{i:02d}. {s}")

    def show_recently_played(self) -> None:
        """Print the recently played songs from newest to oldest."""
        print("--- Recently Played ---")
        if not self.recently_played:
            print("(none yet)")
            return
        # iterate in reverse (newest last appended)
        for i, s in enumerate(reversed(self.recently_played), 1):
            print(f"{i}. {s}")

# ---------- Simple demonstration / test ----------

if __name__ == "__main__":
    # Create playlist
    pl = Playlist("Roadtrip Mix", recently_played_limit=5)

    # Create songs (song info stored as tuple inside each Song object)
    s1 = LocalSong("Drive", "The Cars", 185, file_path="/music/TheCars/Drive.mp3")
    s2 = OnlineSong("Adventure", "Nomad Band", 210, stream_url="https://music.example/nomad/adventure")
    s3 = LocalSong("Sunset", "DJ Calm", 240)
    s4 = OnlineSong("City Lights", "Synth Pop", 198)
    s5 = LocalSong("Homecoming", "Acoustic Duo", 160)

    # Add songs to playlist
    pl.add_song(s1)
    pl.add_song(s2)
    pl.add_song(s3)
    pl.add_song(s4)
    pl.add_song(s5)

    # Show playlist
    pl.show()
    print()

    # Play a couple of songs (demonstrates polymorphism: local/online play)
    pl.play_song(0)  # plays LocalSong 'Drive'
    pl.play_song(1)  # plays OnlineSong 'Adventure'
    print()

    # Show recently played
    pl.show_recently_played()
    print()

    # Shuffle playlist and show the effect
    pl.shuffle()
    pl.show()
    print()

    # Remove a song by name
    pl.remove_song_by_name("Sunset")
    pl.show()
    print()

    # Attempt removing by index
    pl.remove_song_by_index(10)  # out of range
    pl.remove_song_by_index(2)   # valid removal
    pl.show()
    print()

    # Play more songs to fill recently played deque
    pl.play_song(0)
    pl.play_song(0)
    pl.play_next()
    print()

    # Show recently played (should show most recent up to the limit)
    pl.show_recently_played()
