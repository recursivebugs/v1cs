#!/usr/bin/env python3
import requests
import json
import yaml
import os
import sys

def create_ruleset():
    # Use the Container Security API Key instead of a separate token
    API_KEY = os.environ['API_KEY']
    RULESET_FILE = os.environ['RULESET_FILE']
    RULESET_NAME = os.environ.get('RULESET_NAME', 'DemoLogOnlyRuleset')
    
    try:
        with open(RULESET_FILE, 'r') as file:
            # Load the Kubernetes-formatted YAML
            k8s_ruleset = yaml.safe_load(file)
            print("Loaded ruleset data (Kubernetes format):")
            print(json.dumps(k8s_ruleset, indent=2))
            
            # Convert from Kubernetes format to Trend Micro API format
            # Extract the rules from the Kubernetes CR
            rules = []
            if k8s_ruleset.get("spec", {}).get("definition", {}).get("rules"):
                for rule in k8s_ruleset["spec"]["definition"]["rules"]:
                    rules.append({
                        "id": rule.get("ruleID", ""),
                        "action": rule.get("mitigation", "log")
                    })
            
            # Create the properly formatted ruleset for Trend Micro API
            api_ruleset = {
                "name": RULESET_NAME,
                "description": f"Created from {RULESET_FILE}",
                "rules": rules
            }
            
            print("Converted ruleset for API:")
            print(json.dumps(api_ruleset, indent=2))
            
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
        print("Sending request to API...")
        response = requests.post(url, headers=headers, json=api_ruleset)
        
        print(f"API Response Status Code: {response.status_code}")
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
