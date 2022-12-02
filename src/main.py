import requests
import json
import dotenv
import os
from datetime import datetime
import time

# Makes sure that when developing, you do need keep
# spamming the api with requests.
DEV_MODE = True

# Interval between editing in minutes 
POST_DELAY = (30 * 60) # 30 minutes

# Set all these values in a .env file
dotenv.load_dotenv(dotenv.find_dotenv())
SESSION_COOKIE = os.environ["SESSION_COOKIE"] # SESSION_COOKIE: Your AoC Session Cookie
LB_URL = os.environ["LEADERBOARD_URL"] # LEADERBOARD_URL: The private leaderboard url
WEBHOOK_URL = os.environ["WEBHOOK_URL"] # WEBHOOK_URL: The link to the discord webhook
try:
    MESSAGE_ID = os.environ["MESSAGE_ID"] # MESSAGE_ID: The id of the message to edit (has to be webhooks) | optional
except KeyError:
    MESSAGE_ID = None

def get_data() -> dict:
    if DEV_MODE:
        try:
            with open("src/cache.json", "r") as f:
                data = json.load(f)
                print("Using cache")
                return data
        except FileNotFoundError:
            pass
    
    req = requests.get(LB_URL, cookies={
        "session": SESSION_COOKIE,
        "User-Agent": "MAINTAINER GH: @DevFlock; Discord: Flonc#0001"
    })

    if req.status_code != 200:
        raise Exception(f"Status code was non-200: {req.status_code} {req.reason}")

    data = req.json()

    with open("src/cache.json", "w") as f:
        json.dump(data, f, indent=2)
    
    return data

def post_lb():
    data = get_data()

    leaderboard = []
    for member in data["members"]:
        member = data["members"][member]

        stars_str = ""

        for day in member["completion_day_level"]:
            match len(member["completion_day_level"][day]):
                case 0:
                    stars_str += " "
                case 1:
                    stars_str += "🞴"
                case 2:
                    stars_str += "[2;33m🞴[0;33m[0m[2;33m[0m"

        leaderboard.append((member["name"], member["local_score"], stars_str, member["stars"]))
    
    leaderboard.sort(key = lambda x: x[1], reverse=True)

    out = [f"{'Pos': <6}{'Name': <16}{'Score': <10}{'Stars': <3}\n"]

    out[0] = out[0].replace("Pos", "[1;2m[1;34mPos") \
        .replace("Stars", "Stars[0;2m[0m[0m")

    for index, (name, score, stars_str, stars) in enumerate(leaderboard):
        place = str(index+1) + "."
        score, stars = str(score), str(stars)

        out.append(f"{place: <6}{name: <16}{score+'--': <12}{stars+'--': <3}\n{stars_str}\n")

        out[index+1] = out[index+1].replace(place, "[2;35m"+place+"[0;35m[0m[2;35m[0m")\
            .replace(score+'--', "[2;31m"+score+"[0;31m[0m[2;31m[0m")\
            .replace(stars+'--', "[2;31m"+stars+"[0;31m[0m[2;31m[0m")
    
    print("\n".join(out))

    now = datetime.now()
    day = str(now.day)

    webhook_data = {
        "embeds": [
            {
                "title": "Day " + day,
                "image": {
                    "url": "https://media.discordapp.net/attachments/743017609540403211/1048299289752911952/tophat-aoc.png"
                }
            },
            {
                "description": "```ansi\n"+ "\n".join(out) + "```",
                "timestamp": now.isoformat(),
                "footer": {
                    "text": f"Updated every {POST_DELAY//60}:{str(POST_DELAY%60).zfill(2)} minutes"
                }
            }
        ]
    }

    if MESSAGE_ID: 
        req = requests.patch(WEBHOOK_URL + f"/messages/{MESSAGE_ID}", json=webhook_data)
    else:
        req = requests.post(WEBHOOK_URL, json=webhook_data)

    if req.status_code != 200:
        print(f"Status code not 200: {req.status_code} {req.reason}")
    
    else:
        print(f"Leaderboard patch request {req.status_code} {req.reason}") 

post_lb()

while True:
    time.sleep(POST_DELAY)
    post_lb()