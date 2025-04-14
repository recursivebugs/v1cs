import requests
import sys
import os
import json

api_key = os.getenv("API_KEY")
ruleset_id = os.getenv("RULESET_ID")
policy_name = os.getenv("POLICY_NAME")
api_url = os.getenv("API_URL", "https://api.xdr.trendmicro.com/beta/containerSecurity")
policy_file = os.getenv("POLICY_FILE", "trendmicro/policy.json")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

policy_url = f"{api_url}/policies"

try:
    print(f"Creating policy '{policy_name}' with ruleset ID '{ruleset_id}'...")
    print(f"API URL: {policy_url}")
    print(f"Policy file: {policy_file}")
    
    with open(policy_file) as f:
        data = json.load(f)

    data["name"] = policy_name
    
    # Update the ruleset ID in the policy
    if "runtime" in data and "rulesetids" in data["runtime"] and len(data["runtime"]["rulesetids"]) > 0:
        if isinstance(data["runtime"]["rulesetids"][0], dict):
            data["runtime"]["rulesetids"][0]["id"] = ruleset_id
        else:
            # Handle the case where rulesetids is a list of strings
            data["runtime"]["rulesetids"][0] = ruleset_id
    else:
        print("[WARNING] Could not find runtime.rulesetids in policy structure")
        data["runtime"] = {"rulesetids": [{"name": os.getenv("RULESET_NAME"), "id": ruleset_id}]}

    print("📦 Creating Policy with payload:")
    print(json.dumps(data, indent=2))

    res = requests.post(policy_url, headers=headers, json=data)
    print(f"HTTP status code: {res.status_code}")
    print(f"Response: {res.text}")

    if res.status_code == 201:
        try:
            policy_id = res.json().get("id", "unknown")
            print(f"policy_id={policy_id}")
        except Exception:
            print("⚠️ No JSON body in response")
            
        print("✅ Policy created successfully.")
        sys.exit(0)
    else:
        print(f"[ERROR] Failed to create policy: {res.status_code} {res.text}")
        sys.exit(1)

except Exception as e:
    print(f"[EXCEPTION] {e}")
    sys.exit(1)
