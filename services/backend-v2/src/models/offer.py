import time
from pydantic import BaseModel
from pony.orm import PrimaryKey, Required

from src.models import db

class OfferView(BaseModel):
    id: int
    channel_id: int
    text: str = ""
    sended_at: int = int(time.time())

class Offer(db.Entity):
    id = PrimaryKey(int, size=64)
    channel = Required("Channel")
    text = Required(str)
    sended_at = Required(int)

    def toModel(self):
        model = OfferView(id=self.id, channel_id=self.channel.id, text=self.text, sended_at=self.sended_at)
        return model
