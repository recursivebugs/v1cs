#!/bin/bash
set -e

echo "🔍 Checking if policy '$POLICY_NAME' exists..."

resp=$(curl -s -X GET "$API_URL/policies" -H "Authorization: Bearer $API_KEY" -H "Accept: application/json")

if echo "$resp" | jq -e --arg name "$POLICY_NAME" '.items[]? | select(.name == $name)' >/dev/null; then
  echo "✅ Policy exists."
  EXISTS=true
else
  echo "❌ Policy does not exist."
  EXISTS=false
fi
