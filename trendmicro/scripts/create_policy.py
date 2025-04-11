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
                print(f"File content (first 200 chars): {content[:200]}...")
                
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
