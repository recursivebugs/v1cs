import requests
import json
import os
import sys

api_key = os.getenv("API_KEY")
ruleset_name = os.getenv("RULESET_NAME")
api_url = os.getenv("API_URL", "https://api.xdr.trendmicro.com/beta/containerSecurity")
ruleset_path = "trendmicro/runtimeruleset.json"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

ruleset_url = f"{api_url}/rulesets"

try:
    print(f"Creating ruleset '{ruleset_name}'...")
    print(f"API URL: {ruleset_url}")
    
    with open(ruleset_path) as f:
        data = json.load(f)

    data["name"] = ruleset_name

    print("📦 Creating Ruleset with payload:")
    print(json.dumps(data, indent=2))

    res = requests.post(ruleset_url, headers=headers, json=data)
    print(f"HTTP status code: {res.status_code}")
    print(f"Response: {res.text}")

    ruleset_id = ""

    if res.status_code == 201:
        try:
            response_json = res.json()
            ruleset_id = response_json.get("id", "")
            print(f"Ruleset ID from response: {ruleset_id}")
        except Exception:
            print("⚠️ No JSON body found, trying Location header...")
            location = res.headers.get("Location", "")
            ruleset_id = location.split("/")[-1] if location else "unknown"
            print(f"Ruleset ID from location header: {ruleset_id}")

        print(f"id={ruleset_id}")
        print("✅ Ruleset created successfully.")
        sys.exit(0)
    else:
        print(f"[ERROR] Failed to create ruleset: {res.status_code} {res.text}")
        sys.exit(1)

except Exception as e:
    print(f"[EXCEPTION] {e}")
    sys.exit(1)
