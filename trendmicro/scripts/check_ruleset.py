#!/usr/bin/env python3
import requests
import json
import yaml
import os
import sys
import traceback


def load_ruleset_file(ruleset_file_path):
    try:
        with open(ruleset_file_path, 'r') as file:
            if ruleset_file_path.endswith(('.yaml', '.yml')):
                print("Detected YAML format")
                return yaml.safe_load(file)
            elif ruleset_file_path.endswith('.json'):
                print("Detected JSON format")
                return json.load(file)
            else:
                print("Unsupported ruleset file format. Please use .yaml, .yml, or .json")
                sys.exit(1)
    except Exception as e:
        print(f"Error reading ruleset file: {str(e)}")
        traceback.print_exc()
        sys.exit(1)


def check_ruleset():
    try:
        API_KEY = os.environ.get('API_KEY')
        RULESET_NAME = os.environ.get('RULESET_NAME')
        RULESET_FILE = os.environ.get('RULESET_FILE')

        if not API_KEY or not RULESET_NAME or not RULESET_FILE:
            print("Missing required environment variables: API_KEY, RULESET_NAME, RULESET_FILE")
            sys.exit(1)

        print(f"Checking for existing ruleset: {RULESET_NAME}")

        url = f"https://api.xdr.trendmicro.com/beta/containerSecurity/rulesets?name={RULESET_NAME}"
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        }

        response = requests.get(url, headers=headers)

        print(f"API Response Status: {response.status_code}")
        print(f"API Response Body: {response.text}")

        if response.status_code == 200:
            result = response.json()
            if result.get("totalCount", 0) > 0:
                ruleset_id = result["rulesets"][0]["id"]
                print(f"exists=true")
                print(f"ruleset_id={ruleset_id}")
            else:
                print("exists=false")
        else:
            print(f"Failed to check ruleset: HTTP {response.status_code}")
            sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    check_ruleset()
