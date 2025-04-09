#!/usr/bin/env python3

import requests
import json
import os
import sys

def create_ruleset():
    # Use the Container Security API Key instead of a separate token
    API_KEY = os.environ['API_KEY']
    RULESET_FILE = os.environ['RULESET_FILE']

    try:
        with open(RULESET_FILE, 'r') as file:
            ruleset_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: Ruleset file not found at {RULESET_FILE}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in ruleset file {RULESET_FILE}")
        sys.exit(1)
    
    url = "https://api.xdr.trendmicro.com/beta/containerSecurity/rulesets"
    
    headers = {
        'Accept': 'application/json',
        'api-version': 'v1',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(ruleset_data))
    
    if response.status_code != 201:
        print(f"Error creating ruleset: {response.status_code}")
        print(response.text)
        sys.exit(1)
        
    result = response.json()
    
    print(f"Ruleset '{result['name']}' created with ID: {result['id']}")
    print(f"ruleset_id={result['id']}")

if __name__ == "__main__":
    create_ruleset()