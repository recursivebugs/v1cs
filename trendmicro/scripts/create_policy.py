#!/usr/bin/env python3
import requests
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

        if RULESET_ID == "CREATED_BUT_ID_UNKNOWN":
            print("Error: RULESET_ID is invalid or not found. Cannot create policy without a valid ruleset ID.")
            sys.exit(1)

        print(f"RULESET_ID: {RULESET_ID}")
        print(f"Reading policy file: {POLICY_FILE}")

        if not os.path.isfile(POLICY_FILE):
            print(f"Error: Policy file not found at {POLICY_FILE}")
            sys.exit(1)

        with open(POLICY_FILE, 'r') as f:
            payload = f.read()

        print("======== Raw Payload (before modification) ========")
        print(payload)
        print("===================================================")

        # Optional: fix payload if rulesetids is list of objects
        if '"rulesetids": [{' in payload:
            print("Detected rulesetids as objects — fixing to list of strings...")
            import json
            data = json.loads(payload)
            # Flatten rulesetids
            if 'runtime' in data and 'rulesetids' in data['runtime']:
                data['runtime']['rulesetids'] = [RULESET_ID]
            payload = json.dumps(data, indent=2)

        print("======== Final Payload to API ========")
        print(payload)
        print("======================================")

        url = "https://api.xdr.trendmicro.com/beta/containerSecurity/policies"
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        }

        print(f"Sending request to API...")
        print(f"API URL: {url}")
        print("Headers:")
        print(headers)

        response = requests.post(url, headers=headers, data=payload)

        print(f"API Response Status: {response.status_code}")
        print(f"API Response Body: {response.text}")

        if response.status_code in [200, 201]:
            try:
                result = response.json()
                policy_id = result.get('id', 'CREATED_BUT_ID_UNKNOWN')
            except Exception:
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
