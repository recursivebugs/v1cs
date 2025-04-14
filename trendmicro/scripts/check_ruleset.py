import requests
import sys
import os

ruleset_name = os.getenv("RULESET_NAME")
api_key = os.getenv("API_KEY")

url = "https://api.xdr.trendmicro.com/beta/containerSecurity/rulesets"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

try:
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    for r in res.json().get("items", []):
        if r.get("name") == ruleset_name:
            print(f"exists=true id={r['id']}")
            sys.exit(0)
    print("exists=false")
    sys.exit(2)
except Exception as e:
    print(f"[ERROR] Failed to check ruleset: {e}")
    sys.exit(1)
