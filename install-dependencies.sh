#!/bin/bash

# Install dependencies
echo "Installing dependencies..."
apt-get -y update
apt-get -y install \
	curl \
	mono-runtime \
	unzip \
	wget
