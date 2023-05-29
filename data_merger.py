import json
import os
import pandas as pd

# Define the directory path where your JSON files are located
directory = 'auctiondata'

# Initialize an empty list to store all the JSON data
all_data = []

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        # Read the JSON file
        with open(os.path.join(directory, filename), 'r') as file:
            # Load the JSON data
            data = json.load(file)
            # Append the data to the list
            all_data.append(data)

# Write the merged JSON data to a new file
with open('all_auctions.json', 'w') as outfile:
    json.dump(all_data, outfile, indent=4)
