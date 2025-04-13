#!/usr/bin/env python3
import requests
import os
import sys
import traceback

def check_ruleset():
    try:
        API_KEY = os.environ.get('API_KEY')
        RULESET_NAME = os.environ.get('RULESET_NAME')

        if not API_KEY or not RULESET_NAME:
            print("Missing API_KEY or RULESET_NAME env vars")
            sys.exit(2)

        print(f"Checking for existing ruleset: {RULESET_NAME}")

        url = "https://api.xdr.trendmicro.com/beta/containerSecurity/rulesets"
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        }

        response = requests.get(url, headers=headers)
        print(f"API Response Status: {response.status_code}")

        if response.status_code != 200:
            print(f"Error querying API: HTTP {response.status_code}")
            sys.exit(2)

        result = response.json()
        found_id = ""

        for item in result.get("items", []):
            if item.get("name") == RULESET_NAME:
                found_id = item.get("id")
                break

        if found_id:
            print("exists=true")
            print(f"ruleset_id={found_id}")
            sys.exit(0)  # FOUND = exit clean
        else:
            print("exists=false")
            sys.exit(1)  # NOT FOUND = continue

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        traceback.print_exc()
        sys.exit(2)

if __name__ == "__main__":
    check_ruleset()
