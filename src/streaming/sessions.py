"""
sessions.py
-----------
Implement the ListeningSession class for recording listening events.

Classes to implement:
  - ListeningSession
"""

from .users import User
from .tracks import Track
from datetime import datetime

class ListeningSession:
    def __init__(self,session_id,user,track,timestamp,duration):
        self.session_id=session_id
        self.user=user
        self.track=track
        self.timestamp=timestamp
        self.duration_listened_seconds=duration

    def duration_listened_minutes(self):
        return self.duration_listened_seconds/60
