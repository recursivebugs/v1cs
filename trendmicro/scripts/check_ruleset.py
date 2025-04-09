#!/usr/bin/env python3

import requests
import json
import os
import sys

def check_ruleset():
    API_TOKEN = os.environ['API_TOKEN']
    RULESET_NAME = os.environ['RULESET_NAME']

    url = "https://api.xdr.trendmicro.com/beta/containerSecurity/rulesets"
    
    headers = {
        'Accept': 'application/json',
        'api-version': 'v1',
        'Authorization': f'Bearer {API_TOKEN}'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error checking rulesets: {response.status_code}")
        print(response.text)
        sys.exit(1)
        
    rulesets = response.json()
    
    # Check if ruleset exists
    ruleset_exists = False
    ruleset_id = ""
    
    for ruleset in rulesets.get('items', []):
        if ruleset['name'] == RULESET_NAME:
            ruleset_exists = True
            ruleset_id = ruleset['id']
            break
    
    # Output for GitHub Actions
    if ruleset_exists:
        print(f"Ruleset '{RULESET_NAME}' exists with ID: {ruleset_id}")
        print(f"exists=true")
        print(f"ruleset_id={ruleset_id}")
    else:
        print(f"Ruleset '{RULESET_NAME}' does not exist")
        print(f"exists=false")

if __name__ == "__main__":
    check_ruleset()