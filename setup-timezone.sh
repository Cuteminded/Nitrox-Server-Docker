#!/bin/bash

# Configures the timezone
echo "Setting timezone to ${TIMEZONE}..."
ln --symbolic --no-dereference --force /usr/share/zoneinfo/${TIMEZONE} /etc/localtime
echo ${TIMEZONE} > /etc/timezone
