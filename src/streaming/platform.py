"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""

from .playlists import Playlist


class StreamingPlatform:
    def __init__(self, name):
        self.name = name
        self.users = []
        self.tracks = []
        self.artists = []
        self.albums = []
        self.playlists = []
        self.sessions = []

    def add_user(self, user):
        self.users.append(user)

    def add_track(self, track):
        self.tracks.append(track)

    def add_artist(self, artist):
        self.artists.append(artist)

    def add_album(self, album):
        self.albums.append(album)

    def add_playlist(self, playlist):
        self.playlists.append(playlist)

    def add_session(self, session):
        self.sessions.append(session)

    def total_listening_time_minutes(self, start, end):
        total = 0
        for s in self.sessions:
            if start <= s.timestamp <= end:
                total += s.duration_listened_seconds
        return total / 60

    def avg_unique_tracks_per_premium_user(self, days=30):
        from datetime import datetime, timedelta
        from streaming.users import PremiumUser

        cutoff = datetime.now() - timedelta(days=days)

        premium_users = [u for u in self.users if isinstance(u, PremiumUser)]

        if not premium_users:
            return 0.0

        counts = []
        for u in premium_users:
            tracks = {
                s.track.track_id
                for s in u.sessions
                if s.timestamp >= cutoff
            }
            counts.append(len(tracks))

        return sum(counts) / len(counts)

    def track_with_most_distinct_listeners(self):
        if not self.sessions:
            return None

        result = {}
        for s in self.sessions:
            if s.track not in result:
                result[s.track] = set()
            result[s.track].add(s.user)

        return max(result, key=lambda t: len(result[t]))

    def avg_session_duration_by_user_type(self):
        data = {}

        for s in self.sessions:
            user_type = type(s.user).__name__
            if user_type not in data:
                data[user_type]=[]
            data[user_type].append(s.duration_listened_seconds)

        result = [(k, float(sum(v) / len(v))) for k, v in data.items()]
        return sorted(result, key=lambda x: x[1], reverse=True)

    def total_listening_time_underage_sub_users_minutes(self, age_threshold=18):
        from streaming.users import FamilyMember

        total = 0
        for u in self.users:
            if isinstance(u, FamilyMember) and u.age < age_threshold:
                for s in u.sessions:
                    total += s.duration_listened_seconds

        return total / 60

    def all_users(self):
        return self.users

    def top_artists_by_listening_time(self, n=3):
        from streaming.tracks import Song

        result = {}

        for s in self.sessions:
            if isinstance(s.track, Song):
                artist = s.track.artist
                result[artist] = result.get(artist, 0) + s.duration_listened_seconds
        sorted_artists = sorted(result.items(), key=lambda x: x[1], reverse=True)
        return [(a, t / 60) for a, t in sorted_artists[:n]]

    def user_top_genre(self, user_id):
        user = next((u for u in self.users if u.user_id == user_id), None)
        if not user:
            return None

        genre_time = {}
        total = 0

        for s in user.sessions:
            genre = s.track.genre
            genre_time[genre] = genre_time.get(genre, 0) + s.duration_listened_seconds
            total += s.duration_listened_seconds

        if total == 0:
            return None

        top = max(genre_time, key=genre_time.get)
        pct = (genre_time[top] / total) * 100

        return (top, pct)

    def collaborative_playlists_with_many_artists(self, threshold=3):
        result = []

        for p in self.playlists:
            if hasattr(p, "contributors"):
                artists = {t.artist for t in p.tracks if hasattr(t, "artist")}
                if len(artists) > threshold:
                    result.append(p)

        return result

    def avg_tracks_per_playlist_type(self):
        from streaming.playlists import CollaborativePlaylist, Playlist
        normal = [p for p in self.playlists if isinstance(p, Playlist) and not isinstance(p, CollaborativePlaylist)]
        collab = [p for p in self.playlists if isinstance(p, CollaborativePlaylist)]

        return {
            "Playlist": sum(len(p.tracks) for p in normal) / len(normal) if normal else 0.0,
            "CollaborativePlaylist": sum(len(p.tracks) for p in collab) / len(collab) if collab else 0.0,
        }

    def users_who_completed_albums(self):
        result = []

        for u in self.users:
            completed = []

            for album in self.albums:
                album_tracks = {t.track_id for t in album.tracks}
                user_tracks = {s.track.track_id for s in u.sessions}

                if album_tracks and album_tracks.issubset(user_tracks):
                    completed.append(album.title)
            if completed:
                result.append((u, completed))

        return result
