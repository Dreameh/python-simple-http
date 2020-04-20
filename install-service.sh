#!/usr/bin/env bash
# Run this only once!

# Ensure that root runs this script.
if (( $EUID != 0 )); then
    echo "Please run as root"
    exit
fi

cp http-listener.service /etc/systemd/system/
systemctl enable http-listener.service
systemctl start http-listener.service
