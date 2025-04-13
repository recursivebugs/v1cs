#!/usr/bin/env python3

import requests
import os
import sys
import traceback


def check_policy():
    try:
        api_key = os.environ.get('API_KEY')
        policy_name = os.environ.get('POLICY_NAME')

        if not api_key or not policy_name:
            print("Missing API_KEY or POLICY_NAME environment variables.")
            sys.exit(1)

        url = "https://api.xdr.trendmicro.com/beta/containerSecurity/policies"
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

        print(f"Checking if policy '{policy_name}' exists...")

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch policies: HTTP {response.status_code}")
            print(response.text)
            sys.exit(1)

        data = response.json()
        found_id = ""

        for item in data.get("items", []):
            if item.get("name") == policy_name:
                found_id = item.get("id")
                break

        if found_id:
            print("exists=true")
            print(f"policy_id={found_id}")
            sys.exit(0)
        else:
            print("exists=false")
            # Changed from exit code 2 to 0 to prevent GitHub Actions from treating this as an error
            sys.exit(0)

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    check_policy()
