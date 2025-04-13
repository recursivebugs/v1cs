#!/usr/bin/env python3
import requests
import json
import os
import sys


def create_policy():
    api_key = os.getenv('API_KEY')
    policy_name = os.getenv('POLICY_NAME', 'DemoLogOnlyPolicy')
    ruleset_id = os.getenv('RULESET_ID')

    if not api_key or not ruleset_id:
        print("Missing required environment variables.")
        print(f"API_KEY: {'SET' if api_key else 'MISSING'}")
        print(f"RULESET_ID: {ruleset_id or 'MISSING'}")
        sys.exit(1)

    # Create a simplified policy payload directly
    payload = {
        "name": policy_name,
        "description": "A policy with several example logging rules. Created via automation.",
        "default": {
            "rules": [
                {
                    "action": "log",
                    "mitigation": "log",
                    "type": "podSecurityContext",
                    "statement": {
                        "properties": [
                            {
                                "key": "runAsNonRoot",
                                "value": "false"
                            }
                        ]
                    },
                    "enabled": True
                },
                {
                    "action": "log",
                    "mitigation": "log",
                    "type": "containerSecurityContext",
                    "statement": {
                        "properties": [
                            {
                                "key": "privileged",
                                "value": "true"
                            }
                        ]
                    },
                    "enabled": True
                }
            ]
        },
        "runtime": {
            "rulesetids": [ruleset_id]
        },
        "xdrEnabled": True,
        "type": "userManaged",
        "malwareScan": {
            "mitigation": "log",
            "schedule": {
                "enabled": True,
                "cron": "59 3 * * 6"
            }
        }
    }

    # Print the payload for debugging
    print(f"Policy payload: {json.dumps(payload, indent=2)}")

    url = "https://api.xdr.trendmicro.com/beta/containerSecurity/policies"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    print(f"Sending request to create policy: {policy_name}")
    response = requests.post(url, headers=headers, json=payload)

    print(f"API Response Status: {response.status_code}")
    print(f"API Response Body: {response.text}")

    if response.status_code not in [200, 201]:
        print("Failed to create policy")
        sys.exit(1)

    policy_id = response.json().get("id", "CREATED_BUT_ID_UNKNOWN")
    print(f"policy_id={policy_id}")


if __name__ == "__main__":
    create_policy()
