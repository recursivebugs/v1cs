#!/bin/bash
set -e

echo "🚀 Creating Policy '${POLICY_NAME}' using Ruleset ID '${RULESET_ID}'..."

payload=$(jq --arg name "$POLICY_NAME" --arg rid "$RULESET_ID" '.name=$name | .ruleset.id=$rid' trendmicro/payloads/policy.json)

response=$(curl -s -X POST "${API_URL}/policies" -H "Authorization: Bearer ${API_KEY}" -H "accept: application/json" -H "Content-Type: application/json" -d "$payload")

policy_id=$(echo "$response" | jq -r '.id')

if [[ -n "$policy_id" && "$policy_id" != "null" ]]; then
  echo "✅ Policy created: $policy_id"
else
  echo "❌ Failed to create policy."
  exit 1
fi
