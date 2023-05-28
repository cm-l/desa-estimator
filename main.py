# DESA scraper
import json
import time

import requests
from bs4 import BeautifulSoup
# Selenium because of dynamic loading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import url_retriever


def scrape_auctions(url):
    # Configure Selenium WebDriver with Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    # Load the auction results page using Selenium WebDriver
    driver.get(url)
    # This will direct us to the specified URL

    # There's an annoying cookies pop-up. We have to first refuse the saving of cookies to proceed.
    try:
        refusecookies = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[4]/div[1]/div[2]/button[4]")
        refusecookies.click()
        print("Cookies refused!")
    except:
        print("No cookie prompt!")

    time.sleep(1)  # Animation delay (the cookies prompt has to close).
    driver.refresh()  # Refresh page

    # Scroll almost to the bottom of the page using JavaScript so that relevant buttons are in viewport
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.85);")

    # Locate buttons(s) to load every auction
    try:
        ele = driver.find_elements(By.XPATH, '/html/body/div[1]/div[7]/div[2]/div[3]/div/a[2]')
        for x in ele:
            print("Loading button(s) found:", x.tag_name, x.get_attribute("class"))
            time.sleep(5)
            x.click()
            print("Loading button clicked!")
    except:
        print("There was no loading button - that's ok, there's just less items in the auction!")

    time.sleep(5)  # Load delay
    # ALL LOADED CORRECTLY!

    # Get the page source after it has fully loaded
    page_source = driver.page_source

    # Use BeautifulSoup to parse the fully rendered HTML
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the div with the class "search-results list-view"
    search_results_div = soup.find('div', class_='search-results grid-view')

    # Find all the divs within the "search-results list-view" div that contain "desa-object and the debug" in their class
    # names
    divs = search_results_div.find_all('div', class_=lambda x: x and 'desa-object debug__object-published--True' in x)

    # Close the WebDriver
    driver.quit()

    # Parsing data from divs into a nice list of dicts
    auctions = []

    for div in divs:
        auction = {}

        # Extract the name from the div
        name_element = div.find('div', class_='box-object-row__title')
        if name_element:
            name_text = name_element.text.strip()
            first_line = name_text.split('\n')[0]
            auction['author'] = first_line.strip()

        # Extract the title from the div
        title_element = div.find('div', class_='box-object-row__subtitle')
        if title_element:
            auction['title'] = title_element.text.strip()

        # Extract the price from the div
        info_element = div.find('div', class_='box-object-row__info')
        if info_element:
            medium_text = info_element.text.strip()
            parsed_medium = medium_text.split('\n')[0]

            last_comma_index = parsed_medium.rfind(',')
            if last_comma_index != -1:
                only_medium = parsed_medium[:last_comma_index]
                dimensions = parsed_medium[last_comma_index + 1:]
            auction['medium'] = only_medium.strip()
            auction['dimensions'] = dimensions.strip()

            # Extract the hammer price from the info element
            hammer_price_start = 'Hammer price:'
            hammer_price_index = medium_text.find(hammer_price_start)
            if hammer_price_index != -1:
                hammer_price = medium_text[hammer_price_index + len(hammer_price_start):].strip()
                auction['hammer_price'] = hammer_price

        auctions.append(auction)

    # Print the list of auctions
    for auction in auctions:
        print(auction)

    # Save it as a .json file
    # Save `auctions` list to a JSON file and append a part of the link, so I can find it later
    with open(f'auctions_{url.split("/")[-2]}.json', 'w') as json_file:
        json.dump(auctions, json_file, indent=4)

    print("Auctions saved to a local .json file!")


# List of URLs to scrape
urls = url_retriever.get_auction_links()

# Scrape auctions for each URL
for url in urls:
    print(f"Now scraping: {url}")
    scrape_auctions(url)
    print(f"Successfully scraped {url}!")

# https://desa.pl/pl/aukcja-nieruchomosci-augustianska-15/
# This link is a completely different page layout and has to be skipped
# This is a building anyway, not a painting or sculpture lol