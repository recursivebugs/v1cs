#!/bin/bash
set -e

echo "🚀 Creating Policy '$POLICY_NAME' with Ruleset ID '$RULESET_ID'..."

payload=$(jq --arg name "$POLICY_NAME" --arg id "$RULESET_ID" '.name = $name | .runtimeRuleset.id = $id' trendmicro/payloads/policy.json)

resp=$(curl -s -X POST "$API_URL/policies" -H "Authorization: Bearer $API_KEY" -H "Accept: application/json" -H "Content-Type: application/json" -d "$payload")

echo "✅ Created Policy successfully"
