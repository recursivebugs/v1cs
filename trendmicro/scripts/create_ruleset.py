#!/usr/bin/env python3
import requests
import json
import yaml
import os
import sys
import traceback

def create_ruleset():
    try:
        # Get environment variables
        API_KEY = os.environ.get('API_KEY')
        RULESET_FILE = os.environ.get('RULESET_FILE')
        RULESET_NAME = os.environ.get('RULESET_NAME', 'Default Ruleset')
        
        if not API_KEY:
            print("Error: API_KEY environment variable is not set")
            sys.exit(1)
            
        if not RULESET_FILE:
            print("Error: RULESET_FILE environment variable is not set")
            sys.exit(1)
            
        print(f"Reading ruleset file: {RULESET_FILE}")
        
        try:
            with open(RULESET_FILE, 'r') as file:
                content = file.read()
                print(f"File content (first 200 chars): {content[:200]}...")
                
                # Try to parse as YAML
                try:
                    ruleset_data = yaml.safe_load(content)
                    print("Successfully parsed YAML file")
                except Exception as yaml_error:
                    print(f"Error parsing YAML: {str(yaml_error)}")
                    sys.exit(1)
                
                # Extract rules from Kubernetes format
                rules = []
                if ruleset_data and isinstance(ruleset_data, dict):
                    if 'spec' in ruleset_data and 'definition' in ruleset_data['spec'] and 'rules' in ruleset_data['spec']['definition']:
                        rules_data = ruleset_data['spec']['definition']['rules']
                        for rule in rules_data:
                            if 'ruleID' in rule:
                                rule_obj = {
                                    "id": rule.get('ruleID'),
                                    "action": rule.get('mitigation', 'log')
                                }
                                rules.append(rule_obj)
                    
                # Create the API payload
                api_data = {
                    "name": RULESET_NAME,
                    "description": f"Created from {RULESET_FILE}",
                    "rules": rules
                }
                
                print(f"Prepared API request payload: {json.dumps(api_data, indent=2)}")
                
        except FileNotFoundError:
            print(f"Error: File not found at {RULESET_FILE}")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading or parsing file: {str(e)}")
            traceback.print_exc()
            sys.exit(1)
            
        # Make API request
        print("Sending request to API...")
        url = "https://api.xdr.trendmicro.com/beta/containerSecurity/rulesets"
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'api-version': 'v1',
            'Authorization': f'Bearer {API_KEY}'
        }
        
        try:
            response = requests.post(url, headers=headers, json=api_data)
            
            print(f"API Response Status: {response.status_code}")
            print(f"API Response Body: {response.text}")
            
            if response.status_code in [200, 201]:
                try:
                    result = response.json()
                    if isinstance(result, dict) and 'id' in result:
                        print(f"Ruleset created successfully with ID: {result['id']}")
                        print(f"ruleset_id={result['id']}")
                        return
                    else:
                        print(f"API returned success but response format unexpected: {result}")
                except Exception as e:
                    print(f"API returned success but could not parse response: {str(e)}")
                    
                # Use placeholder ID if we can't parse the response
                print("ruleset_id=CREATED_BUT_ID_UNKNOWN")
            else:
                print(f"Error creating ruleset: HTTP {response.status_code}")
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
    create_ruleset()
