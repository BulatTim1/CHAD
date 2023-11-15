import asyncio
from base64 import b64decode
import contextlib
import logging
import time
from typing import NoReturn
from src.config import TELEGRAM_TOKEN
from src.models import *
import telegram as tg
from telegram.error import Forbidden, NetworkError

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def main() -> NoReturn:
    """Run the bot."""
    # Here we use the `async with` syntax to properly initialize and shutdown resources.
    async with tg.Bot(TELEGRAM_TOKEN) as bot:
        # get the first pending update_id, this is so we can skip over it in case
        # we get a "Forbidden" exception.

        logger.info("listening for new messages...")
        while True:
            with db_session:
                messages = select(p for p in Post if p.send_time + 5 <= int(time.time()))
                for message in messages:
                    logger.info(int(time.time()))
                    logger.info(message.send_time)
                    try:
                        if message.media and len(message.media) > 0:
                            if len(message.media) == 1:
                                media = [m for m in message.media][0]
                                if media.type == "photo":
                                        d = media.file
                                        await bot.sendPhoto(message.channel.id, b64decode(d[d.find(b'base64,') + 7:].decode()), caption=message.text)
                                elif media.type == "video":
                                    d = media.file
                                    await bot.sendVideo(message.channel.id, b64decode(d[d.find(b'base64,') + 7:].decode()), caption=message.text)
                            else:
                                media = []
                                first = True
                                for m in message.media:
                                    try:
                                        d = m.file
                                        if m.type == "photo":
                                            media.append(tg.InputMediaPhoto(b64decode(d[d.find(b'base64,') + 7:].decode()), caption=message.text if first else None))
                                        elif m.type == "video":
                                            media.append(tg.InputMediaVideo(b64decode(d[d.find(b'base64,') + 7:].decode()), caption=message.text if first else None))
                                        first = False
                                    except:
                                        print(f"error decoding media {m.id}")
                                await bot.sendMediaGroup(message.channel.id, media)
                        else:
                            await bot.sendMessage(message.channel.id, message.text)
                        message.delete()
                    except NetworkError:
                        await asyncio.sleep(1)
                    except Forbidden:
                        print("error sending message")
                commit()
            await asyncio.sleep(5)

# async def getMessages() -> list[Post]:
#     with db_session:
#         while True:
#             print(int(time.time()))
#             messages = 
#             if messages.count() > 0:
#                 data = messages[:]
#                 print(data)
#                 return data
#             return []

# async def deleteMessage(post: Post) -> bool:
#     with db_session:
#         if post:
#             post.delete()
#             commit()
#             return True
#         return False

if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):  # Ignore exception when Ctrl-C is pressed
        asyncio.run(main())
