#!/usr/bin/env bash
set +e
output=$(python trendmicro/scripts/delete_ruleset.py)
status=$?
echo "$output"

if [ "$status" -eq 0 ]; then
  echo "✅ Ruleset deleted successfully."
else
  echo "🔥 Failed to delete ruleset."
fi
exit $status
