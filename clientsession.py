"""/clientsession.py"""

from datetime import datetime, timezone

class ClientSession:
    def __init__(self, websocket, user_id, username):
        self.websocket = websocket
        self.user_id = user_id
        self.username = username 
        self.joined_at = datetime.now(timezone.utc)
        self.left_at = None
        self.room = None
