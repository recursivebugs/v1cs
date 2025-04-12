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
                    yaml_data = yaml.safe_load(content)
                    print("Successfully parsed YAML file")
                except
