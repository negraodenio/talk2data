import urllib.request
import json

url = "http://localhost:8000/api/chat"
data = json.dumps({"question": "Qual é o target price da BlackRock e o que a OECD diz sobre ela?"}).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

try:
    with urllib.request.urlopen(req) as response:
        result = response.read()
        print("STATUS:", response.status)
        print("BODY:", result.decode("utf-8"))
except Exception as e:
    print("ERROR:", e)
