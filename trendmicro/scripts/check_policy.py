import requests
import sys
import os

policy_name = os.getenv("POLICY_NAME")
api_key = os.getenv("API_KEY")

url = "https://api.xdr.trendmicro.com/beta/containerSecurity/policies"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

try:
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    for item in res.json().get("items", []):
        if item.get("name") == policy_name:
            print(f"Policy '{policy_name}' already exists.")
            sys.exit(1)
    print(f"Policy '{policy_name}' not found.")
    sys.exit(2)
except Exception as e:
    print(f"[ERROR] Failed to check policy: {e}")
    sys.exit(1)
