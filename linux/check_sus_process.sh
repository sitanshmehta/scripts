#!/bin/bash

echo "Checking for suspicious processes..."

# List processes and search for keywords like 'malware', 'mining', or 'crypt'
ps aux | grep -i -E 'malware|mining|crypt'