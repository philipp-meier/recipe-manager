#!/usr/bin/bash

# Get ssh host from the "ssh_host" file (e.g. user@ip-address)
ssh_host=$(cat ssh_host)

# Run unit tests
if ! python3 manage.py test;
then
  echo "Unit tests failed."
  exit 1
fi

# Remove old deployment file
DEPLOYMENT_FILE="./_output/deployment.zip"
if test -f $DEPLOYMENT_FILE; then
  rm deployment.zip
fi

# Create a new deployment file (excluding the database-files)
zip -r $DEPLOYMENT_FILE . -x data/\* media/\* media/recipes/\*

# Deploy the new file to the server
scp $DEPLOYMENT_FILE "$ssh_host":~/Hosting/recipe-manager/

# Stop application
ssh "$ssh_host" "cd ~/Hosting/recipe-manager && docker compose down"

# Extract and add/replace files
ssh "$ssh_host" "cd ~/Hosting/recipe-manager && unzip -o deployment.zip"

# Rebuild the application
ssh "$ssh_host" "cd ~/Hosting/recipe-manager && docker compose build"

# Start the application
ssh "$ssh_host" "cd ~/Hosting/recipe-manager && docker compose up -d"