#!/usr/bin/env python3
import requests
import json
import os
import sys


def create_policy():
    api_key = os.getenv('API_KEY')
    policy_file = os.getenv('POLICY_FILE')
    ruleset_id = os.getenv('RULESET_ID')

    if not api_key or not policy_file or not ruleset_id:
        print("Missing required environment variables.")
        print(f"API_KEY: {'SET' if api_key else 'MISSING'}")
        print(f"POLICY_FILE: {policy_file or 'MISSING'}")
        print(f"RULESET_ID: {ruleset_id or 'MISSING'}")
        sys.exit(1)

    if not os.path.isfile(policy_file):
        print(f"Policy file not found: {policy_file}")
        sys.exit(1)

    # Read the policy file as raw text
    with open(policy_file, 'r') as file:
        policy_content = file.read()
    
    # Replace the ruleset ID in the policy content
    policy_content = policy_content.replace(
        '"rulesetids": [', 
        f'"rulesetids": [\n      "{ruleset_id}"'
    ).replace(
        # Remove any existing ruleset entries
        '      {\n        "name": "DemoLogOnlyRuleset",\n        "id": "DemoLogOnlyRuleset-2vVdMoRvbNhfQx8ZBg1pzDncLAK"\n      }', 
        ''
    )
    
    # Fix the cron expression if needed
    policy_content = policy_content.replace('"cron": "59 3 * *6"', '"cron": "59 3 * * 6"')
    
    # Ensure we don't have empty array brackets after removing items
    policy_content = policy_content.replace('      "",', '').replace('["",', '[')
    policy_content = policy_content.replace('[]', f'["{ruleset_id}"]')
    
    # Debug: Print the policy content
    print(f"Sending policy content: {policy_content}")

    url = "https://api.xdr.trendmicro.com/beta/containerSecurity/policies"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    print(f"Sending request to create policy")
    response = requests.request("POST", url, headers=headers, data=policy_content)

    print(f"API Response Status: {response.status_code}")
    print(f"API Response Body: {response.text}")

    if response.status_code not in [200, 201]:
        print("Failed to create policy")
        sys.exit(1)

    policy_id = response.json().get("id", "CREATED_BUT_ID_UNKNOWN")
    print(f"policy_id={policy_id}")


if __name__ == "__main__":
    create_policy()
