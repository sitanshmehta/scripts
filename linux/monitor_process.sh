#!/bin/bash
# List processes with high CPU or memory usage on macOS

echo "Checking for suspicious processes with high CPU or memory usage..."
output=$(ps aux | awk '$3 > 50 || $4 > 50')

if [[ -n "$output" ]]; then
    echo "Suspicious processes with high CPU or memory usage:"
    echo "$output"
else
    echo "No suspicious processes with high CPU or memory usage found."
fi
