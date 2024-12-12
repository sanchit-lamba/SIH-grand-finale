import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO
from datetime import datetime, timedelta

# Define the start and end dates
start_date = datetime(2021, 1, 1)
end_date = datetime(2024, 12, 10)

# Generate a list of dates
date_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

# Base URL
base_url = "https://www.delhisldc.org/Loaddata.aspx?mode="

# List to store all dataframes
dataframes = []

for date in date_list:
    # Format the date as DD/MM/YYYY
    formatted_date = date.strftime("%d/%m/%Y")
    # Construct the URL
    url = f"{base_url}{formatted_date}"

    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Ensure we catch HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all tables in the webpage
        tables = soup.find_all('table')

        if not tables:
            print(f"No tables found for URL: {url}")
            continue

        for i, table in enumerate(tables):
            try:
                # Wrap the table's HTML in a StringIO object
                table_html = StringIO(str(table))
                # Read the table into a pandas dataframe
                df = pd.read_html(table_html)[0]
                # Add a column for the date
                df['Date'] = formatted_date
                # Append the dataframe to the list
                dataframes.append(df)
            except Exception as e:
                print(f"Error processing table at URL {url}: {e}")
    except Exception as e:
        print(f"Error processing URL {url}: {e}")

# Combine all dataframes into one
if dataframes:
    combined_df = pd.concat(dataframes, ignore_index=True)
    # Save to an Excel file
    output_file = "Combined_Data.xlsx"
    combined_df.to_excel(output_file, index=False)
    print(f"Data successfully saved to {output_file}")
else:
    print("No data extracted.")
