#!/usr/bin/env bash
set -eo pipefail

# Check if ruleset exists
output=$(python trendmicro/scripts/check_ruleset.py)
echo "$output"

if echo "$output" | grep -q "exists=true"; then
  echo "Ruleset '${RULESET_NAME}' already exists. Retrieving ruleset ID..."
  ruleset_id=$(echo "$output" | grep "ruleset_id=" | cut -d'=' -f2)
  echo "Retrieved ruleset ID: ${ruleset_id}"
  export RULESET_ID="${ruleset_id}"
else
  echo "Ruleset '${RULESET_NAME}' doesn't exist. Creating new ruleset..."
  
  # Create ruleset
  output=$(python trendmicro/scripts/create_ruleset.py)
  echo "$output"
  
  # Extract the ruleset ID from the output
  ruleset_id=$(echo "$output" | grep "ruleset_id=" | cut -d'=' -f2)
  echo "Created ruleset with ID: ${ruleset_id}"
  export RULESET_ID="${ruleset_id}"
fi

# Check if policy exists
output=$(python trendmicro/scripts/check_policy.py)
echo "$output"

if echo "$output" | grep -q "exists=true"; then
  echo "Policy '${POLICY_NAME}' already exists. No action needed."
  policy_id=$(echo "$output" | grep "policy_id=" | cut -d'=' -f2)
  echo "Policy ID: ${policy_id}"
else
  echo "Policy '${POLICY_NAME}' doesn't exist. Creating new policy..."
  
  # Create policy
  output=$(python trendmicro/scripts/create_policy.py)
  echo "$output"
  
  policy_id=$(echo "$output" | grep "policy_id=" | cut -d'=' -f2)
  echo "Created policy with ID: ${policy_id}"
fi

echo "Security policies management completed successfully."
