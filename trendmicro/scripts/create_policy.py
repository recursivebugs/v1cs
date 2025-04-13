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

    if not api_key or not policy_file or not ruleset_id:
        print("Missing required environment variables.")
        sys.exit(1)

    if ruleset_id == "CREATED_BUT_ID_UNKNOWN":
        print("Invalid RULESET_ID detected. Exiting.")
        sys.exit(1)

    if not os.path.isfile(policy_file):
        print(f"Policy file not found: {policy_file}")
        sys.exit(1)

    policy_data = load_policy_file(policy_file)

    # Ensure ruleset ID format is correct
    if isinstance(policy_data.get("runtime", {}).get("rulesetids", []), list):
        policy_data["runtime"]["rulesetids"] = [ruleset_id]

    url = "https://api.xdr.trendmicro.com/beta/containerSecurity/policies"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    print(f"Sending request to create policy: {policy_file}")
    response = requests.post(url, headers=headers, json=policy_data)

    print(f"API Response Status: {response.status_code}")
    print(f"API Response Body: {response.text}")

    if response.status_code not in [200, 201]:
        print("Failed to create policy")
        sys.exit(1)

    policy_id = response.json().get("id", "CREATED_BUT_ID_UNKNOWN")
    print(f"policy_id={policy_id}")


if __name__ == "__main__":
    create_policy()
