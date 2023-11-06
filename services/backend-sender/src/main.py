import time, requests
from src.config import *
from src.models import *

def sendPost(post: Post):
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": post.channel.id, "text": post.text})

if __name__ == "__main__":
    while(True):
        with db_session:
            posts = select(p for p in Post if p.send_time + 5 <= int(time.time()))[:]
            print(f"Count: {len(posts)}")
            for p in posts:
                sendPost(p)
                print(f"Sended {p}")
                p.delete()
            commit()
            time.sleep(5)
