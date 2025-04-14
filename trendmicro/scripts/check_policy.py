import requests
import sys
import os

policy_name = os.getenv("POLICY_NAME")
api_key = os.getenv("API_KEY")
api_url = os.getenv("API_URL", "https://api.xdr.trendmicro.com/beta/containerSecurity")

url = f"{api_url}/policies"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

try:
    print(f"Checking if policy '{policy_name}' exists...")
    print(f"API URL: {url}")
    
    res = requests.get(url, headers=headers)
    print(f"Response status code: {res.status_code}")
    
    if res.status_code != 200:
        print(f"Error response: {res.text}")
        sys.exit(1)
    
    policies = res.json().get("items", [])
    print(f"Found {len(policies)} policies")
    
    for item in policies:
        if item.get("name") == policy_name:
            policy_id = item.get("id", "")
            print(f"Policy '{policy_name}' already exists.")
            print(f"exists=true policy_id={policy_id}")
            sys.exit(0)

    print(f"Policy '{policy_name}' not found.")
    print("exists=false")
    sys.exit(0)

except Exception as e:
    print(f"[ERROR] Failed to check policy: {e}")
    sys.exit(1)
