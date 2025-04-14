import requests
import os
import sys

api_key = os.getenv("API_KEY")
ruleset_name = os.getenv("RULESET_NAME")
api_url = os.getenv("API_URL", "https://api.xdr.trendmicro.com/beta/containerSecurity")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

try:
    res = requests.get(f"{api_url}/rulesets", headers=headers)
    print(f"HTTP status code: {res.status_code}")
    
    if res.status_code != 200:
        print(f"Failed to list rulesets: {res.text}")
        sys.exit(1)

    rulesets = res.json().get("items", [])
    for rs in rulesets:
        if rs.get("name") == ruleset_name:
            print(f"exists=true id={rs['id']}")
            sys.exit(0)

    print("exists=false")
    sys.exit(2)

except Exception as e:
    print(f"[EXCEPTION] {e}")
    sys.exit(1)
