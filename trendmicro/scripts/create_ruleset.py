#!/usr/bin/env python3
import requests
import json
import yaml
import os
import sys


def load_ruleset_file(filepath):
    with open(filepath, 'r') as file:
        if filepath.endswith(('.yaml', '.yml')):
            return yaml.safe_load(file)
        return json.load(file)


def create_ruleset():
    api_key = os.getenv('API_KEY')
    ruleset_file = os.getenv('RULESET_FILE')
    ruleset_name = os.getenv('RULESET_NAME')

    if not api_key or not ruleset_file or not ruleset_name:
        print("Missing required environment variables.")
        sys.exit(1)

    if not os.path.isfile(ruleset_file):
        print(f"Ruleset file not found: {ruleset_file}")
        sys.exit(1)

    ruleset_data = load_ruleset_file(ruleset_file)
    rules = [{"id": rule.get('id', ''), "action": rule.get('action', 'log')} for rule in ruleset_data.get('rules', [])]

    payload = {
        "name": ruleset_name,
        "description": f"Created from {ruleset_file}",
        "rules": rules
    }

    url = "https://api.xdr.trendmicro.com/beta/containerSecurity/rulesets"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "api-version": "v1",
        "Authorization": f"Bearer {api_key}"
    }

    print(f"Sending request to create ruleset: {ruleset_name}")
    response = requests.post(url, headers=headers, json=payload)

    print(f"API Response Status: {response.status_code}")
    print(f"API Response Body: {response.text}")

    if response.status_code not in [200, 201]:
        print("Failed to create ruleset")
        sys.exit(1)

    ruleset_id = response.json().get("id", "CREATED_BUT_ID_UNKNOWN")
    print(f"ruleset_id={ruleset_id}")


if __name__ == "__main__":
    create_ruleset()
