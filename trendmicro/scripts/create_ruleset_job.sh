#!/usr/bin/env bash
set +e
output=$(python trendmicro/scripts/create_ruleset.py)
status=$?
echo "$output"

if [ "$status" -eq 0 ]; then
  ruleset_id=$(echo "$output" | grep 'id=' | awk -F'=' '{print $2}' | xargs)
  echo "ruleset_id=$ruleset_id" >> $GITHUB_OUTPUT
else
  echo "🔥 Failed to create ruleset."
fi
exit $status
