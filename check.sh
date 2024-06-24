#!/bin/bash

sqlc compile

if [ $? -eq 0 ]; then
  echo "sqlc compile successful"
  python3 main.py  # Run python script after successful compilation
  sleep 0.2  # Wait for 0.2 seconds
  sqlc generate -f sqlcout.yaml
  if [ $? -eq 0 ]; then
    echo "sqlc generate successful.. emptying query.sql"
    echo > queries/query.sql
  else
    echo "Error: sqlc generate failed"
  fi
else
  echo "Error: sqlc compile failed"
fi
