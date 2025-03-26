# Polygon.io Fivetran Connector Example

This repository contains a custom Fivetran connector for fetching previous day aggregated stock data from the [Polygon.io API](https://polygon.io/). The connector is built using the `fivetran_connector_sdk` and is designed to fetch data for specified stock tickers and load it into a Fivetran destination.

## Features

- Fetches previous day aggregated stock data for specified tickers.
- Handles API rate limits for the free tier of Polygon.io.
- Supports upserting data into a Fivetran destination.
- Includes debugging and deployment scripts for ease of use.

## Prerequisites

- Python 3.8 or higher
- A Polygon.io API key
- A Fivetran account
- `jq` installed on your system (for JSON parsing in shell scripts)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
2. Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt
3. Set up your configuration by updating the config_no_git.json with your Polygon.io API key and the tickers you want to fetch data for:
    ```
    {
        "api_key": "your_polygon_api_key",
        "tickers": "AAPL,MSFT,GOOGL"
    }
    ```

**Note: Do NOT add any credentials to the keys in the configuration.json file as this file is uploaded to get and serves as the template for the Fivetran connection settings.**

## Usage
### Debugging the Connector
To debug the connector locally, run the debug.sh script:
```
    sh debug.sh 
```

This script will:
- Reset the Fivetran connector.
- Copy the config_no_git.json file to the files/ director as configuration.json.
- Run the connector in debug mode.

### Deploying the Connector
To deploy the connector to Fivetran, use the deploy.sh script:
```
sh deploy.sh
```
The script will prompt you for:
- Fivetran account name
- Fivetran destination name
- Fivetran connector name

It will then deploy the connector to Fivetran along with the keys (no values set) in the configuration.json file which appear as settings in the Fivetran UI.  Simply set these values in the Fivetran UI, and start the initial sync.

## Connector Details

### Schema

The connector creates a table named `previous_day_agg` in the destination with the following schema:
- `T` and `t` as the primary keys.
  - "T" represents the ticker symbol.
  - "t" represents the epoch time of the update.
- Additional columns inferred by Fivetran from the Polygon.io API response.

### Rate Limiting

The connector includes logic to handle API rate limits for the free tier of Polygon.io. It pauses for 65 seconds after every 5 API calls (one call per ticker symbol).

### Weekend Handling

The connector skips fetching data if the previous day is a weekend, as the Polygon.io API does not provide data for weekends.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

This repo only serves as a basic example and can be forked and updated as required.

## Acknowledgments

- [Polygon.io](https://polygon.io/) for their API.
- [Fivetran](https://fivetran.com/) for their connector SDK.