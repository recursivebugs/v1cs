#!/usr/bin/env python3

import requests
import os
import sys
import traceback


def check_ruleset():
    try:
        api_key = os.environ.get('API_KEY')
        ruleset_name = os.environ.get('RULESET_NAME')

        if not api_key or not ruleset_name:
            print("Missing API_KEY or RULESET_NAME environment variables.")
            sys.exit(1)

        url = "https://api.xdr.trendmicro.com/beta/containerSecurity/rulesets"
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

        print(f"Checking if ruleset '{ruleset_name}' exists...")

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch rulesets: HTTP {response.status_code}")
            print(response.text)
            sys.exit(1)

        data = response.json()
        found_id = ""

        for item in data.get("items", []):
            if item.get("name") == ruleset_name:
                found_id = item.get("id")
                break

        if found_id:
            print("exists=true")
            print(f"ruleset_id={found_id}")
            sys.exit(0)
        else:
            print("exists=false")
            sys.exit(2)

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    check_ruleset()
