#!/bin/bash
set -e

echo "🔧 DEBUG INFO:"
echo "  - API_URL: $API_URL"
echo "  - RULESET_NAME: $RULESET_NAME"
echo "  - API_KEY length: ${#API_KEY}"
echo "🔍 Checking if ruleset '${RULESET_NAME}' exists..."

if [[ -z "$API_URL" || -z "$API_KEY" || -z "$RULESET_NAME" ]]; then
  echo "❌ Missing required environment variables."
  [[ -z "$API_URL" ]] && echo "  - API_URL is empty"
  [[ -z "$API_KEY" ]] && echo "  - API_KEY is empty"
  [[ -z "$RULESET_NAME" ]] && echo "  - RULESET_NAME is empty"
  exit 1
fi

# Use curl with status capture
response=$(mktemp)
status_code=$(curl -s -o "$response" -w "%{http_code}" -X GET "${API_URL}/runtimeSecurityRulesets" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Accept: application/json")

echo "🌐 HTTP Status: $status_code"

if [[ "$status_code" -ne 200 ]]; then
  echo "❌ Failed to retrieve rulesets. Response:"
  cat "$response"
  exit 5
fi

# Now safe to use jq
ruleset_id=$(jq -r --arg NAME "$RULESET_NAME" '.items[] | select(.name == $NAME) | .id' < "$response")

if [[ -n "$ruleset_id" && "$ruleset_id" != "null" ]]; then
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
