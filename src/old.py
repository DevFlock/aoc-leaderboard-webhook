import requests, json
from datetime import datetime

SESSION_COOKIE = "53616c7465645f5f830e895ba45334164ee29bcd0908322b9dc5aee300ee14c7401aa1bb2a4f92a79f0d3d175b696bf23fbffbb06fe4c9fc1990c4f7cf0123f3"
URL = "https://adventofcode.com/2022/leaderboard/private/view/1461082.json"
WEBHOOK_URL = "https://discord.com/api/webhooks/1048033513082978324/y6v6U-AosOR99ShsEMNb_QfNeMp4VAi8FNhh28R643xhYjAPNwg_8OEbT-vXRrk67aPe"

with open("src/cache.json") as f:
    d = f.read()
    if d:
        print("Using cache")
        data = json.loads(d)
    else:
        print("No cache, requesting data")
        req = requests.get(URL, cookies={"session": SESSION_COOKIE})
        if req.status_code != 200:
            print("Status code not 200")
            print(req.reason)

        data = req.json()
        with open("src/cache.json", "w") as f:
            json.dump(data, f, indent=2)

lb = {}

for member in data["members"]:
    member = data["members"][member]

    lb[member["name"]] = member["local_score"]

lb = dict(sorted(lb.items(), key=lambda item: item[1], reverse=True))

out = [f"{'Pos': <6}{'Name': <15}{'Score': >4}"]
out.append("="*len(out[0]))

for index, member in enumerate(lb):
    score = lb[member]
    place = str(index+1)+"."
    out.append(f"{place: <6}{member: <15}{score: >4}")

print("\n".join(out))

now = datetime.now()
if now.hour < 5:
    day = now.day - 1
else:
    day = now.day

data = {
    "embeds": [{
        f"title": f"🎩 AoC '22 Leaderboard ❄️ - Day {day}",
        "description": "```md\n"+ "\n".join(out) + "```"
    }]
}

requests.post(WEBHOOK_URL, json=data)