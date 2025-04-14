#!/bin/bash
set -e

echo "🧹 Cleaning up Ruleset ID '${RULESET_ID}'..."

curl -s -X DELETE "${API_URL}/managedRules/${RULESET_ID}" -H "Authorization: Bearer ${API_KEY}" -H "accept: application/json"

echo "✅ Ruleset deleted successfully."
