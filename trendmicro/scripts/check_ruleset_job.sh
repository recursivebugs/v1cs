#!/bin/bash
set -e

echo "🔍 Checking if policy '$POLICY_NAME' exists..."

output=$(python trendmicro/scripts/check_policy.py 2>&1)
status=$?

echo "$output"

if [ "$status" -eq 0 ]; then
  echo "✅ Policy '$POLICY_NAME' already exists."
  echo "true" > trendmicro/scripts/check_policy_output.txt
elif [ "$status" -eq 2 ]; then
  echo "🆕 Policy '$POLICY_NAME' not found."
  echo "false" > trendmicro/scripts/check_policy_output.txt
else
  echo "❌ Unknown error while checking policy."
  exit $status
fi
