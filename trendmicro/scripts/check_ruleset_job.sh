#!/bin/bash
set -e

echo "🔍 Checking if ruleset '${RULESET_NAME}' exists..."

response=$(curl -s -X GET "${API_URL}/runtimeSecurityRulesets" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Accept: application/json")

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
