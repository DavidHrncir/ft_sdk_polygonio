from fivetran_connector_sdk import Connector
from fivetran_connector_sdk import Logging as log
from fivetran_connector_sdk import Operations as op
import requests as rq
import pandas as pd
from datetime import date, timedelta
import time
import json

# Define the base URL
BASE_URL = "https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?adjusted=true"

# Define the basic schema using the 
def schema(configuration):
    return [
    {
        "table": "previous_day_agg",  # Name of the table in the destination.
        "primary_key": ["T","t"],  # Primary key column(s) for the table.
        # No columns are defined, meaning the types will be inferred.
    }
    ]

# Function to fetch data from the Polygon.io API
def get_data(api_key, ticker):
    headers = {"Authorization": f"Bearer {api_key}"}
    url = BASE_URL.format(ticker=ticker)

    try:
        response = rq.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        if "results" in data and data["results"]:
            results = data["results"][0]  # Take the first (and only) result
            results["ticker"] = ticker #add ticker to results.
            return pd.DataFrame([results])
        else:
            return pd.DataFrame()  # Return empty DataFrame if no results

    except rq.exceptions.exceptions.RequestException as e:
        log.error(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

# Define the update function
def update(configuration: dict, state: dict):
    log.warning("Polygon.io Previous Day Bar Connector")
    api_key = configuration.get("api_key")
    tickers_str = configuration.get("tickers") #Get tickers from environment variable

    if not api_key:
        raise ValueError("API key is required in configuration.")
    if not tickers_str:
        raise ValueError("tickers is required in configuration.")

    tickers = tickers_str.split(",")  # Split the tickers string into a list

    today = date.today()
    yesterday = today - timedelta(days=1) # The function is for the previous day.

    all_results_df = pd.DataFrame()

    # Only get the ticker if yesterday was a weekday; otherwise, a 404 will occur.
    if not is_weekend(yesterday):
        rateLimit = 0
        for ticker in tickers:
            rateLimit += 1
            if rateLimit % 5 == 0: # Set a minute delay for every 5 calls since the free tier has rate limits per minute.
                time.sleep(65)
            ticker = ticker.strip() #remove leading/trailing whitespace
            results_df = get_data(api_key, ticker)
            if not results_df.empty:
                all_results_df = pd.concat([all_results_df, results_df], ignore_index=True)

        for index, row in all_results_df.iterrows():
            yield op.upsert(table="previous_day_bars", data=row.to_dict())

# Return true if date is weekend.
def is_weekend(date_obj):
  return date_obj.weekday() >= 5

# Create the connector object
connector = Connector(update=update)

# Debugging
if __name__ == "__main__":
    print("########################## Debugging Standard ###########################")
    # Open the configuration.json file and load its contents into a dictionary.
    with open("configuration.json", 'r') as f:
        configuration = json.load(f)
    # Adding this code to your `connector.py` allows you to test your connector by running your file directly from your IDE.
    connector.debug(configuration=configuration)