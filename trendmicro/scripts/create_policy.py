#!/usr/bin/env python3
import requests
import json
import yaml
import os
import sys
import traceback

def create_policy():
    try:
        API_KEY = os.environ.get('API_KEY')
        POLICY_FILE = os.environ.get('POLICY_FILE')
        RULESET_ID = os.environ.get('RULESET_ID')

        if not API_KEY or not POLICY_FILE or not RULESET_ID:
            print("Missing required environment variables: API_KEY, POLICY_FILE, RULESET_ID")
            sys.exit(1)

        print(f"Reading policy file: {POLICY_FILE}")
        print(f"Using ruleset ID: {RULESET_ID}")

        try:
            with open(POLICY_FILE, 'r') as file:
                if POLICY_FILE.endswith(('.yaml', '.yml')):
                    policy_data = yaml.safe_load(file)
                    print("Loaded YAML policy file")
                elif POLICY_FILE.endswith('.json'):
                    policy_data = json.load(file)
                    print("Loaded JSON policy file")
                else:
                    print("Unsupported file format. Please use .yaml, .yml, or .json")
                    sys.exit(1)

        except FileNotFoundError:
            print(f"Error: Policy file not found at {POLICY_FILE}")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading policy file: {str(e)}")
            traceback.print_exc()
            sys.exit(1)

        url = "https://api.xdr.trendmicro.com/beta/containerSecurity/policies"
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        }

        print("Sending request to API...")
        response = requests.post(url, headers=headers, json=policy_data)

        print(f"API Response Status: {response.status_code}")
        print(f"API Response Body: {response.text}")

        if response.status_code in [200, 201]:
            result = response.json()
            print(f"Policy created successfully with ID: {result.get('id', 'UNKNOWN')}")
            print(f"policy_id={result.get('id', 'CREATED_BUT_ID_UNKNOWN')}")
        else:
            print(f"Failed to create policy: HTTP {response.status_code}")
            sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    create_policy()
