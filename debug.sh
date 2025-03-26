#!/bin/bash
echo "Starting debug process..."

echo "Running fivetran reset..."
fivetran reset

echo "Creating files directory..."
mkdir -p files

echo "Copying configuration files to files directory..."
cp -v config_no_git.json files/configuration.json

echo "Contents of files directory:"
ls -la files/

echo "Running fivetran debug..."
fivetran debug