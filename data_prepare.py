import json
import re

import pandas as pd

def prepare_data():
    # Load the JSON file
    with open('all_auctions.json') as file:
        data = json.load(file)

    # Initialize empty lists to store extracted data
    authors = []
    titles = []
    mediums = []
    dimensions = []
    hammer_prices = []

    # 1. CONVERTING DIMENSIONS FROM 123 x 123 cm TO TWO COLUMNS WITH FLOATS
    # 2. REMOVING WRONG PRICE FORMATTING
    # Regular expression pattern to match the desired dimension format
    pattern = r'^[\d.]+ x [\d.]+'

    # Iterate through the nested structure to extract data
    for sublist in data:
        for dictionary in sublist:
            author = dictionary.get("author")
    #        title = dictionary.get("title")
            medium = dictionary.get("medium")
            dimension = dictionary.get("dimensions")
            hammer_price = dictionary.get("hammer_price")

            # Check if the artwork is a painting with two dimensions and has been sold (has a price)
            if dimension.count("x") == 1 and re.match(r'\d+\.?\d* x \d+\.?\d* cm', dimension) and hammer_price is not None:
                # Remove "cm" and other details
                dimension = re.sub(r' cm.*$', '', dimension)

                # Remove commas and "PLN" text from hammer_price
                hammer_price = re.sub(r',', '', hammer_price)
                hammer_price = re.sub(r' PLN', '', hammer_price)

                authors.append(author)
    #            titles.append(title)
                mediums.append(medium)
                dimensions.append(dimension)
                hammer_prices.append(hammer_price)

    # Create a DataFrame from the extracted data
    df = pd.DataFrame({
        "author": authors,
    #    "title": titles,
        "medium": mediums,
        "dimensions": dimensions,
        "hammer_price": hammer_prices
    })

    # Convert hammer_price to numeric format
    df['hammer_price'] = pd.to_numeric(df['hammer_price'])

    # Split the dimensions column into width and height
    df[['width', 'height']] = df['dimensions'].str.split(' x ', expand=True)

    # Clean up the columns
    df['width'] = df['width'].str.strip().astype(float)
    df['height'] = df['height'].str.strip().astype(float)
    df = df.drop('dimensions', axis=1)
    return df


print(prepare_data().iloc[762])