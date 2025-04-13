#!/usr/bin/env python3
import requests
import json
import yaml
import os
import sys


def load_policy_file(filepath):
    with open(filepath, 'r') as file:
        if filepath.endswith(('.yaml', '.yml')):
            return yaml.safe_load(file)
        return json.load(file)


def create_policy():
    api_key = os.getenv('API_KEY')
    policy_file = os.getenv('POLICY_FILE')
    ruleset_id = os.getenv('RULESET_ID')
    policy_name = os.getenv('POLICY_NAME')

    if not api_key or not policy_file or not ruleset_id:
        print("Missing required environment variables.")
        print(f"API_KEY: {'SET' if api_key else 'MISSING'}")
        print(f"POLICY_FILE: {policy_file or 'MISSING'}")
        print(f"RULESET_ID: {ruleset_id or 'MISSING'}")
        sys.exit(1)

    if ruleset_id == "CREATED_BUT_ID_UNKNOWN":
        print("Invalid RULESET_ID detected. Exiting.")
        sys.exit(1)

    if not os.path.isfile(policy_file):
        print(f"Policy file not found: {policy_file}")
        sys.exit(1)

    policy_data = load_policy_file(policy_file)
    
    # Create a simplified policy structure
    simplified_policy = {
        "name": policy_name or policy_data.get("name", ""),
        "description": policy_data.get("description", ""),
        "default": policy_data.get("default", {}),
        "runtime": {
            "rulesetids": [ruleset_id]
        },
        "xdrEnabled": policy_data.get("xdrEnabled", True),
        "type": policy_data.get("type", "userManaged"),
        "malwareScan": {
            "mitigation": policy_data.get("malwareScan", {}).get("mitigation", "log"),
            "schedule": {
                "enabled": True,
                "cron": "59 3 * * 6"  # Fixed cron expression
            }
        }
    }
    
    # Print the policy data for debugging
    print(f"Policy data to be sent: {json.dumps(simplified_policy, indent=2)}")

    url = "https://api.xdr.trendmicro.com/beta/containerSecurity/policies"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    print(f"Sending request to create policy: {policy_file}")
    response = requests.post(url, headers=headers, json=simplified_policy)

    print(f"API Response Status: {response.status_code}")
    print(f"API Response Body: {response.text}")

    if response.status_code not in [200, 201]:
        print("Failed to create policy")
        sys.exit(1)

    policy_id = response.json().get("id", "CREATED_BUT_ID_UNKNOWN")
    print(f"policy_id={policy_id}")


if __name__ == "__main__":
    create_policy()
