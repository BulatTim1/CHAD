from pony.orm import PrimaryKey, Required

from src.models import db

class Post(db.Entity):
    id = PrimaryKey(int, size=64, auto=True)
    text = Required(str)
    send_time = Required(int, size=64)
    channel = Required("Channel")
