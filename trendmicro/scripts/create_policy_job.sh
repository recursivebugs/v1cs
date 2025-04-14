#!/bin/bash
set -e

echo "🔍 Checking if policy '${POLICY_NAME}' exists..."

response=$(curl -s -X GET "${API_URL}/policies" -H "Authorization: Bearer ${API_KEY}" -H "accept: application/json")

if echo "$response" | jq -e --arg name "$POLICY_NAME" '.items[]? | select(.name==$name)' > /dev/null; then
  echo "✅ Policy '${POLICY_NAME}' already exists."
  echo "POLICY_EXISTS=true" >> $GITHUB_ENV
else
  echo "❌ Policy does not exist."
  echo "POLICY_EXISTS=false" >> $GITHUB_ENV
fi
