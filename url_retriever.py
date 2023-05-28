import csv

# Links to all auctions have been previously scraped using Web Scraper and I just load them in from a .csv

import csv
import glob

def get_auction_links():
    folder_path = "auctionlinkings"  # Replace with the path to the folder containing your CSV files
    linking_hrefs = []

    # Get a list of all CSV files in the specified folder
    file_paths = glob.glob(f"{folder_path}/*.csv")

    # Iterate over each file
    for file_path in file_paths:
        with open(file_path, "r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                linking_hrefs.append(row["Linking-href"])

    print(linking_hrefs)
    print(len(linking_hrefs))
    return linking_hrefs