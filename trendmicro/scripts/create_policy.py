#!/usr/bin/env python3
import requests
import json
import yaml
import os
import sys
import traceback

def create_policy():
    try:
        # Get environment variables
        API_KEY = os.environ.get('API_KEY')
        POLICY_FILE = os.environ.get('POLICY_FILE')
        RULESET_ID = os.environ.get('RULESET_ID')
        
        if not API_KEY:
            print("Error: API_KEY environment variable is not set")
            sys.exit(1)
            
        if not POLICY_FILE:
            print("Error: POLICY_FILE environment variable is not set")
            sys.exit(1)
            
        if not RULESET_ID:
            print("Error: RULESET_ID environment variable is not set")
            sys.exit(1)
            
        print(f"Reading policy file: {POLICY_FILE}")
        print(f"Using ruleset ID: {RULESET_ID}")
        
        try:
            # Read the file directly
            with open(POLICY_FILE, 'r') as file:
                policy_yaml = file.read()
                
                # Parse it to make sure it's valid YAML
                policy_data = yaml.safe_load(policy_yaml)
                print(f"Successfully read policy file ({len(policy_yaml)} bytes)")
                
                # Send the policy data as-is to the API
                print("Sending policy data to API without format conversion")
                
        except FileNotFoundError:
            print(f"Error: Policy file not found at {POLICY_FILE}")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {str(e)}")
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
            # Send the policy data as-is
            response = requests.post(url, headers=headers, json=policy_data)
            
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
