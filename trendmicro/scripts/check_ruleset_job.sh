#!/bin/bash
set -e

echo "🔧 DEBUG INFO:"
echo " - API_URL: ${API_URL}"
echo " - RULESET_NAME: ${RULESET_NAME}"
echo " - API_KEY length: ${#API_KEY}"

echo "🔍 Checking if ruleset '${RULESET_NAME}' exists..."

response=$(curl -s -H "Authorization: Bearer ${API_KEY}" "${API_URL}/managedRules?top=100")

if echo "$response" | jq -e --arg name "$RULESET_NAME" '.items[] | select(.name == $name)' > /dev/null; then
  ruleset_id=$(echo "$response" | jq -r --arg name "$RULESET_NAME" '.items[] | select(.name == $name) | .id')
  echo "✅ Ruleset found: ${ruleset_id}"
  exists=true
else
  echo "❌ Ruleset does not exist."
  exists=false
fi

echo "exists=$exists" >> $GITHUB_OUTPUT

if [ "$exists" = "true" ]; then
  echo "ruleset_id=${ruleset_id}" >> $GITHUB_OUTPUT
fi
