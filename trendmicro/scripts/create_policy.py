#!/usr/bin/env python3
import requests
import os
import sys
import traceback
import re

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
            # Read the file content directly without parsing
            with open(POLICY_FILE, 'r') as file:
                policy_content = file.read()
                print(f"File content length: {len(policy_content)} characters")
                
                # Replace any RULESET_ID placeholder with the actual ID
                policy_content = policy_content.replace("RULESET_ID_PLACEHOLDER", RULESET_ID)
                
                # Print a portion of the content for debugging
                print("Policy content (first 500 chars):")
                print(policy_content[:500])
                print("...")
                
        except FileNotFoundError:
            print(f"Error: File not found at {POLICY_FILE}")
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
            response = requests.post(url, headers=headers, data=policy_content)
            
            print(f"API Response Status: {response.status_code}")
            print(f"API Response Headers: {response.headers}")
            print(f"API Response Body: {response.text}")
            
            if response.status_code in [200, 201]:
                # Extract ID from response
                try:
                    import json
                    result = json.loads(response.text)
                    if isinstance(result, dict) and 'id' in result:
                        print(f"Policy created successfully with ID: {result['id']}")
                        print(f"policy_id={result['id']}")
                        return
                    else:
                        print(f"API returned success but response format unexpected: {result}")
                except Exception as e:
                    print(f"API returned success but could not parse response: {str(e)}")
                    
                # Use regex to try to extract ID directly from the response text
                id_match = re.search(r'"id"\s*:\s*"([^"]+)"', response.text)
                if id_match:
                    policy_id = id_match.group(1)
                    print(f"Extracted policy ID from response: {policy_id}")
                    print(f"policy_id={policy_id}")
                    return
                    
                # Use placeholder ID if we can't parse the response
                print("policy_id=CREATED_BUT_ID_UNKNOWN")
            else:
                print(f"Error creating policy: HTTP {response.status_code}")
                print(f"Response: {response.text}")
                
                # Add more detailed error information
                print("\nPossible issues:")
                print("1. The policy format might not be valid JSON")
                print("2. The ruleset ID might not be valid or might not exist")
                print("3. There might be other validation issues with the policy structure")
                
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
