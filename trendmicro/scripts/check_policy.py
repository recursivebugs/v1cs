#!/usr/bin/env python3
import requests
import os
import sys
import json

def check_policy():
    API_KEY = os.environ.get('API_KEY')
    POLICY_NAME = os.environ.get('POLICY_NAME')

    if not API_KEY or not POLICY_NAME:
        print("Missing API_KEY or POLICY_NAME env vars")
        sys.exit(1)

    print(f"Checking for existing policy: {POLICY_NAME}")

    url = "https://api.xdr.trendmicro.com/beta/containerSecurity/policies"
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }

    response = requests.get(url, headers=headers)

    print(f"API Response Status: {response.status_code}")
    print(f"API Response Body: {response.text}")

    if response.status_code != 200:
        print("Error querying API")
        sys.exit(1)

    result = response.json()

    for item in result.get("items", []):
        if item.get("name") == POLICY_NAME:
            print(f"Policy with name '{POLICY_NAME}' already exists with ID: {item.get('id')}")
            sys.exit(0)

    print("Policy does not exist")
    sys.exit(2)

if __name__ == "__main__":
    check_policy()
