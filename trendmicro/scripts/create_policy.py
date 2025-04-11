#!/usr/bin/env python3

import requests
import json
import os
import sys

def create_policy():
    # Use the Container Security API Key instead of a separate token
    API_KEY = os.environ['API_KEY']
    POLICY_FILE = os.environ['POLICY_FILE']
    RULESET_ID = os.environ['RULESET_ID']
    
    try:
        with open(POLICY_FILE, 'r') as file:
            policy_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: Policy file not found at {POLICY_FILE}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in policy file {POLICY_FILE}")
        sys.exit(1)
    
    # Replace placeholder with actual ruleset ID
    if "ruleset" in policy_data and policy_data["ruleset"] == "RULESET_ID_PLACEHOLDER":
        policy_data["ruleset"] = RULESET_ID
    
    url = "https://api.xdr.trendmicro.com/beta/containerSecurity/policies"
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(policy_data))
    
    if response.status_code not in [200, 201]:
        print(f"Error creating policy: {response.status_code}")
        print(response.text)
        sys.exit(1)
        
    result = response.json()
    
    print(f"Policy '{result['name']}' created with ID: {result['id']}")
    print(f"policy_id={result['id']}")

if __name__ == "__main__":
    create_policy()