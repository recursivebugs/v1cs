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
    
    # Verify the ruleset ID is not empty
    if not ruleset_id:
        print("[ERROR] Ruleset ID is empty. Cannot create policy.")
        sys.exit(1)
    
    # Read the policy file and verify it exists
    if not os.path.exists(policy_file):
        print(f"[ERROR] Policy file '{policy_file}' not found.")
        sys.exit(1)
    
    with open(policy_file) as f:
        file_content = f.read()
        print(f"Policy file content ({len(file_content)} bytes):")
        print(file_content[:500] + "..." if len(file_content) > 500 else file_content)
        
        # Try to parse the JSON
        try:
            data = json.loads(file_content)
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON in policy file: {e}")
            sys.exit(1)

    # Set the policy name
    data["name"] = policy_name
    
    # Update the ruleset ID in the policy
    ruleset_updated = False
    
    # Check for various possible structures in the policy JSON
    if "runtime" in data and "rulesetids" in data["runtime"]:
        if isinstance(data["runtime"]["rulesetids"], list):
            if len(data["runtime"]["rulesetids"]) > 0:
                if isinstance(data["runtime"]["rulesetids"][0], dict) and "id" in data["runtime"]["rulesetids"][0]:
                    data["runtime"]["rulesetids"][0]["id"] = ruleset_id
                    ruleset_updated = True
                    print(f"Updated ruleset ID in rulesetids[0].id")
                elif isinstance(data["runtime"]["rulesetids"][0], str):
                    data["runtime"]["rulesetids"][0] = ruleset_id
                    ruleset_updated = True
                    print(f"Updated ruleset ID in rulesetids[0] (string)")
            else:
                data["runtime"]["rulesetids"].append({"name": os.getenv("RULESET_NAME", "DemoLogOnlyRuleset"), "id": ruleset_id})
                ruleset_updated = True
                print(f"Added new ruleset ID to empty rulesetids array")
    
    # If we couldn't update the ruleset ID using the existing structure, create the structure
    if not ruleset_updated:
        print("[WARNING] Could not find runtime.rulesetids in policy structure, creating it")
        data["runtime"] = {"rulesetids": [{"name": os.getenv("RULESET_NAME", "DemoLogOnlyRuleset"), "id": ruleset_id}]}

    print("📦 Final policy payload:")
    print(json.dumps(data, indent=2))

    # Make the API request to create the policy
    res = requests.post(policy_url, headers=headers, json=data)
    print(f"HTTP status code: {res.status_code}")
    print(f"Response headers: {dict(res.headers)}")
    print(f"Response body: {res.text}")

    if res.status_code in [200, 201]:
        try:
            policy_id = res.json().get("id", "unknown")
            print(f"policy_id={policy_id}")
        except Exception as e:
            print(f"⚠️ Could not parse response JSON: {e}")
            if "Location" in res.headers:
                policy_id = res.headers["Location"].split("/")[-1]
                print(f"policy_id={policy_id} (from Location header)")
            
        print("✅ Policy created successfully.")
        sys.exit(0)
    else:
        print(f"[ERROR] Failed to create policy: {res.status_code} {res.text}")
        sys.exit(1)

except Exception as e:
    print(f"[EXCEPTION] {e}")
    import traceback
    print(traceback.format_exc())
    sys.exit(1)
