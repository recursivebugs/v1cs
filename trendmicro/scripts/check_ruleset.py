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
    print(f"Checking if ruleset '{ruleset_name}' exists...")
    print(f"API URL: {api_url}")
    
    res = requests.get(f"{api_url}/rulesets", headers=headers)
    print(f"Response status code: {res.status_code}")
    
    if res.status_code != 200:
        print(f"Error response: {res.text}")
        sys.exit(1)

    rulesets = res.json().get("items", [])
    print(f"Found {len(rulesets)} rulesets")
    
    for rs in rulesets:
        if rs.get("name") == ruleset_name:
            ruleset_id = rs.get("id", "")
            print(f"Ruleset '{ruleset_name}' exists with ID: {ruleset_id}")
            print(f"exists=true id={ruleset_id}")
            sys.exit(0)

    print(f"Ruleset '{ruleset_name}' not found.")
    print("exists=false")
    sys.exit(0)

except Exception as e:
    print(f"[ERROR] Failed to check ruleset: {e}")
    sys.exit(1)
