#!/bin/bash

# Remove existing user
echo "Removing existing user..."
userdel nitrox || true
groupdel nitrox || true

# Create the user group
echo "Creating Nitrox user group with ID ${GROUP_ID}..."
groupadd --gid ${GROUP_ID} nitrox

# Create the user
echo "Creating Nitrox user account with ID ${USER_ID}..."
useradd --gid ${GROUP_ID} --uid ${USER_ID} --home-dir /software/nitrox nitrox

# Change the active user
echo "Switching to Nitrox user..."
su - nitrox
