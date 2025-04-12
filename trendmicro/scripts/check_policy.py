#!/usr/bin/env python3

import requests
import json
import os
import sys
import traceback


def check_policy():
    try:
        API_KEY = os.environ.get('API_KEY')
        POLICY_NAME = os.environ.get('POLICY_NAME')

        if not API_KEY or not POLICY_NAME:
            print("Missing API_KEY or POLICY_NAME env vars")
            sys.exit(1)

        url = "https://api.xdr.trendmicro.com/beta/containerSecurity/policies"

        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        }

        print(f"Checking for existing policy: {POLICY_NAME}")
        print(f"API URL: {url}")
        print(f"API Headers: {json.dumps(headers, indent=2)}")

        response = requests.get(url, headers=headers)

        print(f"API Response Status: {response.status_code}")
        print(f"API Response Body: {response.text}")

        if response.status_code != 200:
            print(f"Error checking policies: HTTP {response.status_code}")
            sys.exit(1)

        policies = response.json()

        policy_exists = False
        policy_id = ""

        for policy in policies.get('items', []):
            if policy.get('name') == POLICY_NAME:
                policy_exists = True
                policy_id = policy.get('id')
                break

        if policy_exists:
            print(f"Policy '{POLICY_NAME}' exists with ID: {policy_id}")
            print("exists=true")
            print(f"policy_id={policy_id}")
        else:
            print(f"Policy '{POLICY_NAME}' does not exist")
            print("exists=false")

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    check_policy()
