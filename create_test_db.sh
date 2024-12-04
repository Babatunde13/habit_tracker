#!/bin/bash

echo "Creating database tracker_test..."
psql -U tracker -d tracker -h localhost -c "CREATE DATABASE tracker_test;"
echo "Database tracker_test created successfully"
echo "Database name is tracker_test"