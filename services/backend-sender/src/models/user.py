from pony.orm import PrimaryKey, Required, Set

from src.models import db

class User(db.Entity):
    id = PrimaryKey(int, size=64)
    first_name = Required(str)
    username = Required(str)
    photo_url = Required(str)
    auth_date = Required(int, size=64)
    channels = Set("Channel")
