from src.config import TELEGRAM_TOKEN, TELEGRAM_BOT_ID
import requests

base_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN.decode()}"


def getNewChannels(userId, channelsIds=[]):
    try:
        resp = requests.get(
            f"{base_url}/getUpdates", json={"allowed_updates": ["my_chat_member"]}
        ).json()
        for res in resp["result"]:
            try:
                print(res)
                if (
                    "my_chat_member" in res.keys()
                    and "new_chat_member" in res["my_chat_member"].keys()
                    and res["my_chat_member"]["from"]["id"] == userId
                    and res["my_chat_member"]["new_chat_member"]["status"] == "administrator"
                    and res["my_chat_member"]["chat"]["id"] not in channelsIds
                ):
                    return {
                        "id": res["my_chat_member"]["chat"]["id"],
                        "title": res["my_chat_member"]["chat"]["title"],
                    }
            except:
                continue
        return {}
    except:
        return {}

def getChatAdmins(channelId):
    try:
        resp = requests.get(
            f"{base_url}/getChatAdministrators", json={"chat_id": channelId}
        ).json()
        admins = []
        if resp["ok"] == True:
            for res in resp["result"]:
                if res["user"]["is_bot"] != True:
                    admins.append(res["user"]["id"])
        return admins
    except:
        return []
