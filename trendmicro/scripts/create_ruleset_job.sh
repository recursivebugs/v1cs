#!/bin/bash
set -e

echo "🚀 Creating Ruleset '$RULESET_NAME'..."

payload=$(jq --arg name "$RULESET_NAME" '.name = $name' trendmicro/payloads/ruleset.json)

resp=$(curl -s -X POST "$API_URL/managedRules" -H "Authorization: Bearer $API_KEY" -H "Accept: application/json" -H "Content-Type: application/json" -d "$payload")

RULESET_ID=$(echo "$resp" | jq -r '.id')

echo "✅ Created Ruleset with ID: $RULESET_ID"
