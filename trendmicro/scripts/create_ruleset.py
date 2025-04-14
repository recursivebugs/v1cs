import requests
import sys
import os
import json

api_key = os.getenv("API_KEY")
ruleset_name = os.getenv("RULESET_NAME")
ruleset_path = "trendmicro/runtimeruleset.json"

url = "https://api.xdr.trendmicro.com/beta/containerSecurity/rulesets"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

try:
    with open(ruleset_path) as f:
        data = json.load(f)

    data["name"] = ruleset_name

    res = requests.post(url, headers=headers, json=data)
    res.raise_for_status()
    ruleset_id = res.json()["id"]
    print(f"ruleset_id={ruleset_id}")
    sys.exit(0)
except Exception as e:
    print(f"[ERROR] Failed to create ruleset: {e}")
    sys.exit(1)
