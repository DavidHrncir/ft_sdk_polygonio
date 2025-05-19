#!/bin/bash

# Get the config path env var. This is the path where the keys are located for the FT accounts.
CONFIG_PATH="${FT_CONFIG_KEY_PATH}"
CONFIG_FILE="ft_accounts_config.json"

# Prompt for the Fivetran Account Name (default is current dbx hol acct)
read -p "Enter your Fivetran Account Name [MDS_DATABRICKS_HOL]: " ACCOUNT_NAME
ACCOUNT_NAME=${ACCOUNT_NAME:-"MDS_DATABRICKS_HOL"}

# Read API key from ft_accounts_config.json based on account name
API_KEY=$(jq -r ".fivetran.$ACCOUNT_NAME.api_key" "$CONFIG_PATH/$CONFIG_FILE")

if [ "$API_KEY" == "null" ]; then
    echo "Error: Account name not found in $CONFIG_PATH/$CONFIG_FILE"
    exit 1
fi

# Prompt for the Fivetran Destination Name (default is current dbx dest)
CONFIG_DEST_NAME=$(jq -r ".fivetran.$ACCOUNT_NAME.dest_name" "$CONFIG_PATH/$CONFIG_FILE")
read -p "Enter your Fivetran Destination Name [$CONFIG_DEST_NAME]: " DESTINATION_NAME
DESTINATION_NAME=${DESTINATION_NAME:-"$CONFIG_DEST_NAME"}

# Prompt for the Fivetran Connector Name
read -p "Enter a unique Fivetran Connector Name [default-connection]: " CONNECTION_NAME
CONNECTION_NAME=${CONNECTION_NAME:-"default-connection"}

# Deploy with configuration file
fivetran deploy --api-key "$API_KEY" --destination "$DESTINATION_NAME" --connection "$CONNECTION_NAME" --configuration configuration.json