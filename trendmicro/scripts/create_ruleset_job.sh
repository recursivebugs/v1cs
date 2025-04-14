#!/bin/bash
set -e

echo "🚀 Creating Ruleset '${RULESET_NAME}'..."

payload=$(jq --arg name "$RULESET_NAME" '.name=$name' trendmicro/payloads/ruleset.json)

response=$(curl -s -X POST "${API_URL}/managedRules" -H "Authorization: Bearer ${API_KEY}" -H "accept: application/json" -H "Content-Type: application/json" -d "$payload")

ruleset_id=$(echo "$response" | jq -r '.id')

if [[ -n "$ruleset_id" && "$ruleset_id" != "null" ]]; then
  echo "✅ Ruleset created: $ruleset_id"
  echo "RULESET_ID=$ruleset_id" >> $GITHUB_ENV
else
  echo "❌ Failed to create ruleset."
  exit 1
fi
