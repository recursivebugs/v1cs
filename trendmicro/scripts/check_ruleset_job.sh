#!/bin/bash
set -e

echo "🔍 Checking if ruleset '$RULESET_NAME' exists..."

resp=$(curl -s -X GET "$API_URL/managedRules" -H "Authorization: Bearer $API_KEY" -H "Accept: application/json")

RULESET_ID=$(echo "$resp" | jq -r --arg name "$RULESET_NAME" '.items[]? | select(.name == $name) | .id')

if [ -n "$RULESET_ID" ] && [ "$RULESET_ID" != "null" ]; then
  echo "✅ Ruleset exists."
  EXISTS=true
else
  echo "❌ Ruleset does not exist."
  EXISTS=false
fi
