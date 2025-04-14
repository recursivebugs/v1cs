#!/usr/bin/env bash
set +e
output=$(python trendmicro/scripts/check_policy.py)
status=$?
echo "$output"

if [ "$status" -eq 0 ]; then
  id=$(echo "$output" | awk -F'id=' '{print $2}' | xargs)
  echo "exists=true" >> $GITHUB_OUTPUT
  echo "policy_id=$id" >> $GITHUB_OUTPUT
elif [ "$status" -eq 2 ]; then
  echo "exists=false" >> $GITHUB_OUTPUT
else
  echo "🔥 Failed to check policy."
  exit $status
fi
exit 0
