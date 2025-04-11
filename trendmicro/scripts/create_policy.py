#!/usr/bin/env python3
import requests
import json
import yaml
import os
import sys

def create_policy():
    # Use the Container Security API Key instead of a separate token
    API_KEY = os.environ['API_KEY']
    POLICY_FILE = os.environ['POLICY_FILE']
    RULESET_ID = os.environ['RULESET_ID']
    
    try:
        with open(POLICY_FILE, 'r') as file:
            # Try YAML first
            try:
                policy_data = yaml.safe_load(file)
                print("Loaded policy data as YAML:")
            except yaml.YAMLError:
                # Fall back to JSON
                file.seek(0)
                policy_data = json.load(file)
                print("Loaded policy data as JSON:")
                
            print(json.dumps(policy_data, indent=2))
                
            # Check if this is a Kubernetes-style YAML
            if "apiVersion" in policy_data and "kind" in policy_data and "metadata" in policy_data:
                print("Converting Kubernetes format to API format...")
                # Extract relevant data from Kubernetes format
                api_policy = {
                    "name": policy_data.get("metadata", {}).get("name", "Default Policy"),
                    "description": "Converted from Kubernetes format",
                    "ruleset": RULESET_ID
                }
                
                # Extract any other necessary fields
                if "spec" in policy_data:
                    if "labels" in policy_data["spec"]:
                        api_policy["labels"] = policy_data["spec"]["labels"]
                
                policy_data = api_policy
                print("Converted policy data:")
                print(json.dumps(policy_data, indent=2))
            
            # Ensure the ruleset ID is set
            if "ruleset" in policy_data and policy_data["ruleset"] == "RULESET_ID_PLACEHOLDER":
                policy_data["ruleset"] = RULESET_ID
                
    except FileNotFoundError:
        print(f"Error: Policy file not found at {POLICY_FILE}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Could not parse file {POLICY_FILE}: {str(e)}")
        sys.exit(1)
    
    url = "https://api.xdr.trendmicro.com/beta/containerSecurity/policies"
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    
    try:
        print("Sending policy request to API...")
        response = requests.post(url, headers=headers, json=policy_data)
        
        print(f"API Response Status Code: {response.status_code}")
        print(f"API Response Headers: {response.headers}")
        print(f"API Response Body: {response.text}")
        
        if response.status_code not in [200, 201]:
            print(f"Error creating policy: {response.status_code}")
            print(response.text)
            sys.exit(1)
            
        # Check if response body is empty or not JSON
        if not response.text.strip():
            print("API returned empty response body with success status code")
            print("policy_id=CREATED_BUT_ID_UNKNOWN")
            return
            
        try:
            result = response.json()
            print(f"Policy '{result['name']}' created with ID: {result['id']}")
            print(f"policy_id={result['id']}")
        except json.JSONDecodeError:
            print("Warning: API returned success but response is not valid JSON")
            print("Response Body:", response.text)
            print("policy_id=CREATED_BUT_ID_UNKNOWN")
            
    except Exception as e:
        print(f"Error making API request: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    create_policy()
