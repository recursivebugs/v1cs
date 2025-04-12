#!/usr/bin/env python3
import requests
import json
import yaml
import os
import sys
import traceback


def load_policy_file(policy_file_path):
    try:
        with open(policy_file_path, 'r') as file:
            if policy_file_path.endswith(('.yaml', '.yml')):
                print("Detected YAML format")
                return yaml.safe_load(file)
            elif policy_file_path.endswith('.json'):
                print("Detected JSON format")
                return json.load(file)
            else:
                print("Unsupported policy file format. Please use .yaml, .yml, or .json")
                sys.exit(1)
    except Exception as e:
        print(f"Error reading policy file: {str(e)}")
        traceback.print_exc()
        sys.exit(1)


def create_policy():
    try:
        API_KEY = os.environ.get('API_KEY')
        POLICY_FILE = os.environ.get('POLICY_FILE')
        RULESET_ID = os.environ.get('RULESET_ID')

        if not API_KEY or not POLICY_FILE or not RULESET_ID:
            print("Missing required environment variables: API_KEY, POLICY_FILE, RULESET_ID")
            sys.exit(1)

        if RULESET_ID == "CREATED_BUT_ID_UNKNOWN":
            print("ERROR: RULESET_ID is invalid or not found. Cannot create policy without a valid RULESET_ID.")
            sys.exit(1)

        print(f"Reading policy file: {POLICY_FILE}")
        print(f"Using RULESET_ID: {RULESET_ID}")

        if not os.path.isfile(POLICY_FILE):
            print(f"Error: Policy file not found at {POLICY_FILE}")
            sys.exit(1)

        policy_data = load_policy_file(POLICY_FILE)

        # Always enforce correct rulesetid format for API
        if "runtime" in policy_data and "rulesetids" in policy_data["runtime"]:
            print("Cleaning runtime.rulesetids to contain only the RULESET_ID...")
            policy_data["runtime"]["rulesetids"] = [RULESET_ID]

        url = "https://api.xdr.trendmicro.com/beta/containerSecurity/policies"
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        }

        print("Sending request to API...")
        print(f"API URL: {url}")
        print(f"API Headers: {json.dumps(headers, indent=2)}")
        print(f"API Payload:")
        print(json.dumps(policy_data, indent=2))

        response = requests.post(url, headers=headers, json=policy_data)

        print(f"API Response Status: {response.status_code}")
        print(f"API Response Body: {response.text}")

        if response.status_code in [200, 201]:
            if response.text.strip():
                try:
                    result = response.json()
                    policy_id = result.get('id', 'CREATED_BUT_ID_UNKNOWN')
                except Exception:
                    policy_id = 'CREATED_BUT_ID_UNKNOWN'
            else:
                policy_id = 'CREATED_BUT_ID_UNKNOWN'

            print(f"Policy created successfully with ID: {policy_id}")
            print(f"policy_id={policy_id}")

        else:
            print(f"Failed to create policy: HTTP {response.status_code}")
            sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    create_policy()
