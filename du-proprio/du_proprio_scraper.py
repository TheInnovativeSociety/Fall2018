# --------------------------------#
#     Fall 2018 | Web Scraper     #
# --------------------------------#

# Objectives 											

# Find "for sale" housing information	 
# duproprio.com						

# Libraries
import requests
from bs4 import BeautifulSoup
from csv import writer
import re

# Set page count (maximum available at time of writing: 2163 pages)
maxPage = 2163

# "Open" csv to write header
with open('du_proprio_scraped.csv', "w") as csv_file:
    csv_writer = writer(csv_file)
    csv_writer.writerow(["Rent Price", "Address", "Location", "Number of Bed", "Number of Bath", "Living Area (ft^2)", "Land Area (ft^2)"])

# Add link
for pgnum in range(1,maxPage+1):
    url = "https://duproprio.com/fr/rechercher/liste?search=true&is_for_sale=1&with_builders=1&parent=1&pageNumber=" + str(pgnum) + "&sort=-published_at"

    # Initial scraper setup
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    container = soup.find(class_="container")
    posting_list = container.find(class_="search-results-listings-list")

    # List of postings
    posting_elements = posting_list.find_all(class_="search-results-listings-list__item")

    # "Open" csv to start writing scraped data
    with open("du_proprio_scraped.csv", "a") as csv_file:
        csv_writer = writer(csv_file)

        # Scrape desired variables from individual ads on search page "search-results-listings-list__item"
        for posting in posting_elements:
            # Prices
            posting_price_elem = posting.find(class_="search-results-listings-list__item-description__price")
            # Location
            location_elem = posting.find(class_="search-results-listings-list__item-description__item search-results-listings-list__item-description__city")
            # Address
            address_elem = posting.find(class_="search-results-listings-list__item-description__item search-results-listings-list__item-description__address")
            # Other characteristics
            characteristic_elem = posting.find_all(class_="search-results-listings-list__item-description__characteristics__item")

            # Extracting individual elements for each variable scraped above.
            if posting_price_elem is not None:
                price_val = posting_price_elem.find("h2").text.replace('$', '').rstrip()

            if location_elem is not None:
                location_val = location_elem.find("span").text

            if address_elem is not None:
                address_val = address_elem.text.strip(' \t\n\r') # Strip unwanted values from address output

            # Dealing with un-formatted output from website (cutting out whitespace and splitting at integer value)
            for char in characteristic_elem:
                if char is not None:
                    # Set search criteria
                    criteria = re.compile("([a-zA-Z]+)([0-9]+)")
                    # Split concatonated string into string and integer components
                    char_name = criteria.match(re.sub(r"\W", "", char.text)).group(1)
                    char_val = criteria.match(re.sub(r"\W", "", char.text)).group(2)

                if char_name == 'Chambres':
                    bed_val = char_val
                elif char_name == 'SallesdebainSallesdeau':
                    if char_val in ('11', '21', '31', '41', '51', '61', '12', '22', '32', '42', '52', '62'):  # Taking care of the "+1" and "+2" bathroom cases
                        bath_val = char_val[0] + "+" + char_val[1]
                    else:
                        bath_val = char_val
                elif char_name == 'Airehabitablessolexclu':
                    livingarea_val = char_val
                elif char_name == 'Tailleduterrain':
                    land_val = char_val

                    # Write to csv file
                    csv_writer.writerow([price_val, address_val, location_val, bed_val, bath_val, livingarea_val, land_val])

# End
