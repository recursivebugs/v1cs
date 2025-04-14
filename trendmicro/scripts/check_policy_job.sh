#!/bin/bash
set -e

echo "Checking if policy '${POLICY_NAME}' exists..."

response=$(curl -s -X GET "${API_URL}/policies" \
    -H "Authorization: Bearer ${API_KEY}" \
    -H "Accept: application/json")

exists="false"
for name in $(echo "$response" | jq -r '.items[].name'); do
  if [[ "$name" == "$POLICY_NAME" ]]; then
    exists="true"
    break
  fi
done

echo "Policy exists? ${exists}"

# Export variable to GitHub Actions outputs
echo "exists=${exists}" >> $GITHUB_OUTPUT

echo "### Check Policy Job" >> $GITHUB_STEP_SUMMARY
echo "" >> $GITHUB_STEP_SUMMARY
echo "Policy Name: ${POLICY_NAME}" >> $GITHUB_STEP_SUMMARY
echo "Exists: ${exists}" >> $GITHUB_STEP_SUMMARY
