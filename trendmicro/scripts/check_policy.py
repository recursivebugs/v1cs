#!/usr/bin/env python3

import requests
import json
import os
import sys

def check_policy():
    # Use the Container Security API Key instead of a separate token
    API_KEY = os.environ['API_KEY']
    POLICY_NAME = os.environ['POLICY_NAME']

    url = "https://api.xdr.trendmicro.com/beta/containerSecurity/policies"
    
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error checking policies: {response.status_code}")
        print(response.text)
        sys.exit(1)
        
    policies = response.json()
    
    # Check if policy exists
    policy_exists = False
    policy_id = ""
    
    for policy in policies.get('items', []):
        if policy['name'] == POLICY_NAME:
            policy_exists = True
            policy_id = policy['id']
            break
    
    # Output for GitHub Actions
    if policy_exists:
        print(f"Policy '{POLICY_NAME}' exists with ID: {policy_id}")
        print(f"exists=true")
        print(f"policy_id={policy_id}")
    else:
        print(f"Policy '{POLICY_NAME}' does not exist")
        print(f"exists=false")

if __name__ == "__main__":
    check_policy()