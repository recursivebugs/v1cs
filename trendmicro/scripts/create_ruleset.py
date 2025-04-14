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

    print(f"HTTP status code: {res.status_code}")
    print(f"Response text: {res.text}")

    if res.status_code != 201:
        print(f"[ERROR] Failed to create ruleset: {res.status_code} {res.text}")
        sys.exit(1)

    json_data = res.json()
    ruleset_id = json_data.get("id")

    if not ruleset_id:
        print("[ERROR] Ruleset created but ID not found in response.")
        sys.exit(1)

    print(f"ruleset_id={ruleset_id}")
    sys.exit(0)

except Exception as e:
    print(f"[ERROR] Exception during ruleset creation: {e}")
    sys.exit(1)
