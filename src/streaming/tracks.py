"""
tracks.py
---------
Implement the class hierarchy for all playable content on the platform.

Classes to implement:
  - Track (abstract base class)
    - Song
      - SingleRelease
      - AlbumTrack
    - Podcast
      - InterviewEpisode
      - NarrativeEpisode
    - AudiobookTrack
"""
class Track:
    def __init__(self, track_id, title, duration, genre):
        self.track_id = track_id
        self.title=title
        self.duration=duration
        self.genre=genre

    def duration_minutes(self):
        return self.duration/60

    def __eq__(self,other):
        if not isinstance(other,Track):
            return False
        return self.track_id==other.track_id

class Song(Track):
    def __init__(self,track_id,title,duration,genre,artist):
        super().__init__(track_id,title,duration,genre)
        self.album=None
        self.artist=artist

class SingleRelease(Song):
    def __init__(self,track_id,title,duration,genre,artist,release_date):
        super().__init__(track_id,title,duration,genre,artist)
        self.release_date=release_date

class AlbumTrack(Song):
    def __init__(self,track_id,title,duration,genre,artist,track_number):
        super().__init__(track_id,title,duration,genre,artist)
        self.track_number=track_number
        self.album=None

class Podcast(Track):
    def __init__(self,track_id,title,duration,genre,host):
        super().__init__(track_id,title,duration,genre)
        self.host = host
        self.description=""

class InterviewEpisode(Podcast):
    def __init__(self,track_id,title,duration,genre,host,guest):
        super().__init__(track_id,title,duration,genre,host)
        self.guest=guest

class NarrativeEpisode(Podcast):
    def __init__(self,track_id,title,duration,genre,host,season,episode_number):
        super().__init__(track_id,title,duration,genre,host)
        self.season=season
        self.episode_number=episode_number

class AudiobookTrack(Track):
    def __init__(self,track_id,title,duration,genre,author,narrator):
        super().__init__(track_id,title,duration,genre)
        self.author=author
        self.narrator=narrator
