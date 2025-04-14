import requests
import sys
import os

api_key = os.getenv("API_KEY")
ruleset_id = os.getenv("RULESET_ID")

url = f"https://api.xdr.trendmicro.com/beta/containerSecurity/rulesets/{ruleset_id}"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

try:
    res = requests.delete(url, headers=headers)
    if res.status_code == 204:
        print(f"Ruleset {ruleset_id} deleted.")
        sys.exit(0)
    else:
        print(f"[ERROR] Failed to delete ruleset: {res.status_code} {res.text}")
        sys.exit(1)
except Exception as e:
    print(f"[ERROR] Exception during deletion: {e}")
    sys.exit(1)
