#!/bin/bash
set -e

echo "🔍 Checking if ruleset '${RULESET_NAME}' exists..."

response=$(curl -s -X GET "${API_URL}/managedRules" -H "Authorization: Bearer ${API_KEY}" -H "accept: application/json")

ruleset_id=$(echo "$response" | jq -r --arg name "$RULESET_NAME" '.items[]? | select(.name==$name) | .id')

if [[ -n "$ruleset_id" && "$ruleset_id" != "null" ]]; then
  echo "✅ Ruleset found: $ruleset_id"
  echo "RULESET_EXISTS=true" >> $GITHUB_ENV
  echo "RULESET_ID=$ruleset_id" >> $GITHUB_ENV
else
  echo "❌ Ruleset does not exist."
  echo "RULESET_EXISTS=false" >> $GITHUB_ENV
fi
