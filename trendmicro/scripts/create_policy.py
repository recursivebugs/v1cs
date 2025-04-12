#!/usr/bin/env python3
import requests
import json
import os
import sys
import traceback

def create_policy():
    try:
        # Get environment variables
        API_KEY = os.environ.get('API_KEY')
        POLICY_FILE = "trendmicro/policy.json"  # Hardcode to use the JSON file instead
        RULESET_ID = os.environ.get('RULESET_ID')
        
        if not API_KEY:
            print("Error: API_KEY environment variable is not set")
            sys.exit(1)
            
        if not RULESET_ID:
            print("Error: RULESET_ID environment variable is not set")
            sys.exit(1)
            
        print(f"Reading policy file: {POLICY_FILE}")
        print(f"Using ruleset ID: {RULESET_ID}")
        
        try:
            # Read the JSON file
            with open(POLICY_FILE, 'r') as file:
                try:
                    policy_data = json.load(file)
                    print("Successfully loaded JSON policy file")
                    
                    # Update the ruleset ID in the policy
                    if "runtime" in policy_data and "rulesetids" in policy_data["runtime"] and len(policy_data["runtime"]["rulesetids"]) > 0:
                        print("Updating ruleset ID in policy...")
                        policy_data["runtime"]["rulesetids"][0]["id"] = RULESET_ID
                    
                    # Convert back to JSON with proper formatting
                    policy_json = json.dumps(policy_data)
                    print(f"Prepared policy payload (first 500 chars):")
                    print(policy_json[:500])
                    
                except json.JSONDecodeError as e:
                    print(f"Error: Invalid JSON in policy file: {str(e)}")
                    sys.exit(1)
                
        except FileNotFoundError:
            print(f"Error: Policy file not found at {POLICY_FILE}")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading policy file: {str(e)}")
            traceback.print_exc()
            sys.exit(1)
            
        # Make API request
        print("Sending request to API...")
        url = "https://api.xdr.trendmicro.com/beta/containerSecurity/policies"
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        }
        
        try:
            response = requests.post(url, headers=headers, data=policy_json)
            
            print(f"API Response Status: {response.status_code}")
            print(f"API Response Headers: {response.headers}")
            print(f"API Response Body: {response.text}")
            
            if response.status_code in [200, 201]:
                try:
                    result = json.loads(response.text)
                    if isinstance(result, dict) and 'id' in result:
                        print(f"Policy created successfully with ID: {result['id']}")
                        print(f"policy_id={result['id']}")
                        return
                    else:
                        print(f"API returned success but response format unexpected: {result}")
                except Exception as e:
                    print(f"API returned success but could not parse response: {str(e)}")
                    
                # Use placeholder ID if we can't parse the response
                print("policy_id=CREATED_BUT_ID_UNKNOWN")
            else:
                print(f"Error creating policy: HTTP {response.status_code}")
                print(f"Response: {response.text}")
                sys.exit(1)
                
        except Exception as e:
            print(f"Error making API request: {str(e)}")
            traceback.print_exc()
            sys.exit(1)
            
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    create_policy()
