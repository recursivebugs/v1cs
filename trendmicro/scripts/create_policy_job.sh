#!/usr/bin/env bash
set +e
output=$(python trendmicro/scripts/create_policy.py)
status=$?
echo "$output"

if [ "$status" -eq 0 ]; then
  policy_id=$(echo "$output" | grep 'policy_id=' | awk -F'=' '{print $2}' | xargs)
  echo "policy_id=$policy_id" >> $GITHUB_OUTPUT
else
  echo "🔥 Failed to create policy."
fi
exit $status
