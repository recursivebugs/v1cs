#!/bin/bash
set -e

echo "🔧 DEBUG INFO:"
echo "  - API_URL: $API_URL"
echo "  - RULESET_NAME: $RULESET_NAME"
echo "  - API_KEY length: ${#API_KEY}"  # Do not echo the actual key for security
echo "🔍 Checking if ruleset '${RULESET_NAME}' exists..."

# Ensure required environment variables are set
if [[ -z "$API_URL" || -z "$API_KEY" || -z "$RULESET_NAME" ]]; then
  echo "❌ Missing required environment variables."
  [[ -z "$API_URL" ]] && echo "  - API_URL is empty"
  [[ -z "$API_KEY" ]] && echo "  - API_KEY is empty"
  [[ -z "$RULESET_NAME" ]] && echo "  - RULESET_NAME is empty"
  exit 1
fi

response=$(curl -s -X GET "${API_URL}/runtimeSecurityRulesets" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Accept: application/json")

# Show snippet of response for debug (limited to 300 chars to avoid flooding log)
echo "🧾 Partial API Response: $(echo "$response" | cut -c 1-300)..."

ruleset_id=$(echo "$response" | jq -r --arg NAME "$RULESET_NAME" '.items[] | select(.name == $NAME) | .id')

if [ -n "$ruleset_id" ]; then
  echo "✅ Ruleset '${RULESET_NAME}' exists with id: $ruleset_id"
  echo "exists=true" >> $GITHUB_OUTPUT
  echo "ruleset_id=$ruleset_id" >> $GITHUB_OUTPUT
  exit 0
else
  echo "❌ Ruleset '${RULESET_NAME}' not found."
  echo "exists=false" >> $GITHUB_OUTPUT
  echo "ruleset_id=" >> $GITHUB_OUTPUT
  exit 2
fi
