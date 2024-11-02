#!/usr/bin/env python3

import subprocess
import csv
import os
import datetime
import sys
from pathlib import Path
import difflib

def get_active_ips():
    result = subprocess.run(
        ["lsof", "-i", "-n", "-P"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        print("Error executing lsof command:", result.stderr)
        sys.exit(1)

    lines = result.stdout.strip().split('\n')

    ips = set()
    for line in lines[1:]:
        parts = line.split()
        if len(parts) >= 9:
            ip_port = parts[8]
            if '->' in ip_port:
                remote_ip_port = ip_port.split('->')[-1]
                ip = remote_ip_port.split(':')[0]
                ips.add(ip)
            elif ':' in ip_port:
                ip = ip_port.split(':')[0]
                ips.add(ip)
    return ips

def load_previous_ips(filepath):
    if not os.path.exists(filepath):
        return set()
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        previous_ips = set(row[0] for row in reader)
    return previous_ips

def save_current_ips(ips, filepath):
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        for ip in sorted(ips):
            writer.writerow([ip])

def send_notification(new_ips):
    message = f"New IP addresses detected:\n{', '.join(new_ips)}"
    subprocess.run([
        "osascript", "-e",
        f'display notification "{message}" with title "IP Monitor"'
    ])

def main():
    data_dir = Path.home() / ".ip_monitor"
    data_dir.mkdir(exist_ok=True)
    current_file = data_dir / "current_ips.csv"
    previous_file = data_dir / "previous_ips.csv"

    current_ips = get_active_ips()
    previous_ips = load_previous_ips(previous_file)
    save_current_ips(current_ips, current_file)

    new_ips = current_ips - previous_ips
    if new_ips:
        send_notification(new_ips)

    current_file.replace(previous_file)

if __name__ == "__main__":
    main()
