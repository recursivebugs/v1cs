#!/usr/bin/env python3
import requests
import json
import yaml  # Add YAML support
import os
import sys

def create_ruleset():
    # Use the Container Security API Key instead of a separate token
    API_KEY = os.environ['API_KEY']
    RULESET_FILE = os.environ['RULESET_FILE']
    
    try:
        with open(RULESET_FILE, 'r') as file:
            # Try to load as YAML
            ruleset_data = yaml.safe_load(file)
            
            # Print the data for debugging
            print("Loaded ruleset data:")
            print(json.dumps(ruleset_data, indent=2))
            
            # Ensure required fields are present
            if "name" not in ruleset_data:
                print("Error: 'name' field is required in ruleset")
                sys.exit(1)
            
            # Create a properly formatted ruleset object that the API expects
            formatted_ruleset = {
                "name": ruleset_data.get("name"),
                "description": ruleset_data.get("description", ""),
                "profiles": ruleset_data.get("profiles", [])
            }
            
            # Print the formatted data
            print("Formatted ruleset data:")
            print(json.dumps(formatted_ruleset, indent=2))
            
    except FileNotFoundError:
        print(f"Error: Ruleset file not found at {RULESET_FILE}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in ruleset file {RULESET_FILE}: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Could not parse file {RULESET_FILE}: {str(e)}")
        sys.exit(1)
    
    url = "https://api.xdr.trendmicro.com/beta/containerSecurity/rulesets"
    
    headers = {
        'Accept': 'application/json',
        'api-version': 'v1',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    
    try:
        response = requests.post(url, headers=headers, json=formatted_ruleset)
        
        print(f"API Response Status Code: {response.status_code}")
        print(f"API Response Headers: {response.headers}")
        print(f"API Response Body: {response.text}")
        
        if response.status_code != 201:
            print(f"Error creating ruleset: {response.status_code}")
            print(response.text)
            sys.exit(1)
            
        result = response.json()
        
        print(f"Ruleset '{result['name']}' created with ID: {result['id']}")
        print(f"ruleset_id={result['id']}")
    except Exception as e:
        print(f"Error making API request: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    create_ruleset()
