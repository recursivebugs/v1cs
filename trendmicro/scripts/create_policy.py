import requests
import sys
import os
import json

api_key = os.getenv("API_KEY")
ruleset_name = os.getenv("RULESET_NAME")
policy_name = os.getenv("POLICY_NAME")
policy_path = "trendmicro/policy.json"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

ruleset_url = "https://api.xdr.trendmicro.com/beta/containerSecurity/rulesets"
policy_url = "https://api.xdr.trendmicro.com/beta/containerSecurity/policies"

try:
    res = requests.get(ruleset_url, headers=headers)
    res.raise_for_status()
    rulesets = res.json().get("items", [])

    ruleset_id = None
    for r in rulesets:
        if r.get("name") == ruleset_name:
            ruleset_id = r.get("id")
            break

    if not ruleset_id:
        print(f"[ERROR] Ruleset with name '{ruleset_name}' not found.")
        sys.exit(1)

    print(f"✅ Found ruleset ID: {ruleset_id}")

    with open(policy_path) as f:
        data = json.load(f)

    data["name"] = policy_name
    if "runtime" in data and "rulesetids" in data["runtime"] and len(data["runtime"]["rulesetids"]) > 0:
        data["runtime"]["rulesetids"][0]["id"] = ruleset_id
    else:
        print("[ERROR] Missing 'runtime.rulesetids[0]' structure in policy.json")
        sys.exit(1)

    print("📦 Final Payload:")
    print(json.dumps(data, indent=2))

    res = requests.post(policy_url, headers=headers, json=data)
    print(f"HTTP status code: {res.status_code}")
    print(f"Response: {res.text}")

    if res.status_code == 201:
        policy_id = res.json().get("id", "unknown")
        print(f"policy_id={policy_id}")
        print("✅ Policy created successfully.")
        sys.exit(0)
    else:
        print(f"[ERROR] Failed to create policy: {res.status_code} {res.text}")
        sys.exit(1)

except Exception as e:
    print(f"[EXCEPTION] {e}")
    sys.exit(1)
