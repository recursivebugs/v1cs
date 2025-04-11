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
            with open(POLICY_FILE, 'r') as file:
                content = file.read()
                print(f"File content length: {len(content)} characters")
                
                # Try to parse as YAML
                try:
                    policy_data = yaml.safe_load(content)
                    print("Successfully parsed YAML file")
                except Exception as yaml_error:
                    print(f"Error parsing YAML: {str(yaml_error)}")
                    sys.exit(1)
                
                # Extract policy details from Kubernetes format
                api_policy = {}
                if policy_data and isinstance(policy_data, dict):
                    if 'apiVersion' in policy_data and 'kind' in policy_data and 'metadata' in policy_data:
                        # This is a Kubernetes custom resource
                        print("Detected Kubernetes format, converting...")
                        api_policy = {
                            "name": policy_data.get("metadata", {}).get("name", "Default Policy"),
                            "description": "Converted from Kubernetes format",
                            "ruleset": RULESET_ID
                        }
                        
                        # Extract additional fields if present
                        if "spec" in policy_data:
                            if "labels" in policy_data["spec"]:
                                api_policy["labels"] = policy_data["spec"]["labels"]
                    else:
                        # This is probably already in API format
                        api_policy = policy_data
                        # Ensure ruleset ID is set
                        if "ruleset" in api_policy:
                            if api_policy["ruleset"] == "RULESET_ID_PLACEHOLDER":
                                api_policy["ruleset"] = RULESET_ID
                        else:
                            api_policy["ruleset"] = RULESET_ID
                
                print(f"Prepared API request payload:")
                print(json.dumps(api_policy, indent=2))
                
        except FileNotFoundError:
            print(f"Error: File not found at {POLICY_FILE}")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading or parsing file: {str(e)}")
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
            response = requests.post(url, headers=headers, json=api_policy)
            
            print(f"API Response Status: {response.status_code}")
            print(f"API Response Headers: {response.headers}")
            print(f"API Response Body: {response.text}")
            
            if response.status_code in [200, 201]:
                try:
                    result = response.json()
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
