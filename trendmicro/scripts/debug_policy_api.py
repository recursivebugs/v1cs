#!/usr/bin/env python3
import requests
import json
import os
import sys
import hashlib
import re

def debug_request():
    # Get environment variables
    api_key = os.getenv('API_KEY')
    policy_file = os.getenv('POLICY_FILE')
    ruleset_id = os.getenv('RULESET_ID')
    
    print("=== DEBUG INFO ===")
    print(f"API_KEY present: {'Yes' if api_key else 'No'}")
    print(f"API_KEY length: {len(api_key) if api_key else 'N/A'}")
    print(f"API_KEY hash: {hashlib.sha256(api_key.encode()).hexdigest()[:10] if api_key else 'N/A'}")
    print(f"POLICY_FILE: {policy_file}")
    print(f"RULESET_ID: {ruleset_id}")
    
    # Check if policy file exists
    if not os.path.isfile(policy_file):
        print(f"ERROR: Policy file not found: {policy_file}")
        sys.exit(1)
        
    # Read the policy file as raw text
    with open(policy_file, 'r') as file:
        policy_content = file.read()
    
    # Print file info
    print(f"Policy file size: {len(policy_content)} bytes")
    print(f"Policy file hash: {hashlib.sha256(policy_content.encode()).hexdigest()[:10]}")
    
    # Use regex to fix the cron expression
    policy_content = re.sub(r'"cron":\s*"59\s+3\s+\*\s+\*6"', '"cron": "59 3 * * 6"', policy_content)
    
    # Check if ruleset ID exists in the policy
    if "DemoLogOnlyRuleset-" in policy_content:
        print("Found existing ruleset ID in policy file")
        
        # Extract the existing ruleset ID pattern
        existing_id_match = re.search(r'"id"\s*:\s*"(DemoLogOnlyRuleset-[^"]+)"', policy_content)
        if existing_id_match:
            existing_id = existing_id_match.group(1)
            print(f"Existing ruleset ID: {existing_id}")
            
            # Replace the existing ID with the new one
            policy_content = policy_content.replace(existing_id, ruleset_id)
            print(f"Replaced with new ruleset ID: {ruleset_id}")
    else:
        print("No existing ruleset ID found. Looking for rulesetids array...")
        
        # Look for rulesetids array
        if '"rulesetids": [' in policy_content:
            print("Found rulesetids array")
            
            # Replace the rulesetids array content
            policy_content = re.sub(
                r'"rulesetids"\s*:\s*\[\s*(\{[^}]+\}\s*,?\s*)*\]',
                f'"rulesetids": ["{ruleset_id}"]',
                policy_content
            )
            print("Updated rulesetids array")
    
    # Validate that the policy content is valid JSON
    try:
        json_obj = json.loads(policy_content)
        print("Policy content is valid JSON")
        
        # Check if rulesetids is set correctly
        if "runtime" in json_obj and "rulesetids" in json_obj["runtime"]:
            print(f"rulesetids in JSON: {json_obj['runtime']['rulesetids']}")
        else:
            print("WARNING: rulesetids not found in JSON structure")
            
        # Check cron format
        if "malwareScan" in json_obj and "schedule" in json_obj["malwareScan"] and "cron" in json_obj["malwareScan"]["schedule"]:
            print(f"cron in JSON: {json_obj['malwareScan']['schedule']['cron']}")
        else:
            print("WARNING: cron not found in JSON structure")
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {str(e)}")
        print(f"Location: Line {e.lineno}, Column {e.colno}")
        print(f"Context: {e.doc[max(0, e.pos-20):e.pos+20]}")
        sys.exit(1)
    
    # Try making requests with different approaches
    url = "https://api.xdr.trendmicro.com/beta/containerSecurity/policies"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # Approach 1: Using requests.post with json parameter
    print("\n=== APPROACH 1: requests.post with json parameter ===")
    try:
        response1 = requests.post(url, headers=headers, json=json_obj)
        print(f"Status: {response1.status_code}")
        print(f"Response: {response1.text}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Approach 2: Using requests.request with data parameter
    print("\n=== APPROACH 2: requests.request with data parameter ===")
    try:
        response2 = requests.request("POST", url, headers=headers, data=policy_content)
        print(f"Status: {response2.status_code}")
        print(f"Response: {response2.text}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Approach 3: Using requests.post with data parameter and json.dumps
    print("\n=== APPROACH 3: requests.post with data=json.dumps ===")
    try:
        response3 = requests.post(url, headers=headers, data=json.dumps(json_obj))
        print(f"Status: {response3.status_code}")
        print(f"Response: {response3.text}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Create a minimal policy to test
    print("\n=== APPROACH 4: Minimal policy JSON ===")
    minimal_policy = {
        "name": "MinimalTestPolicy",
        "description": "Minimal test policy",
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
    
    try:
        response4 = requests.post(url, headers=headers, json=minimal_policy)
        print(f"Status: {response4.status_code}")
        print(f"Response: {response4.text}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Create a successful policy based on the one we know works
    print("\n=== NEXT STEPS ===")
    if response4.status_code in [200, 201]:
        print("Minimal policy creation SUCCESSFUL! Use this approach in create_policy.py")
    else:
        print("All approaches failed. Possible issues:")
        print("1. API key might be incorrect or expired")
        print("2. There might be an issue with the ruleset ID format")
        print("3. The API endpoint might have specific requirements we're missing")
        print("4. Check if there are any rate limits or IP restrictions")
    
    print("\n=== END DEBUG ===")

if __name__ == "__main__":
    debug_request()
