# DISC
# Web Scraper
# Fall 2018

# Objective: find rent price, location, length of post, bed/bath, footprint

# Packages
import requests
from bs4 import BeautifulSoup
from csv import writer

# duproprio.ca
response = requests.get("https://duproprio.com/fr/rechercher/liste?search=true&cities%5B0%5D=1885&is_for_sale=1&with_builders=1&parent=1&sort=-published_at")
soup = BeautifulSoup(response.text, "html.parser")
container = soup.find(class_="container")
posting_list = container.find(class_="search-results-listings-list")
posting_elements = posting_list.find_all(class_="search-results-listings-list__item")

with open("../Data/du_proprio_scrape.csv", "w") as csv_file:
	csv_writer = writer(csv_file)
	csv_writer.writerow(["Rent Price", "Location", "Length of Post", "# Bed/Bath", "Footprint"])

	for posting in posting_elements:
		posting_price_elem = posting.find(class_="search-results-listings-list__item-description__price")

		if posting_price_elem is not None:
			price_val = posting_price_elem.find("h2").text	
			csv_writer.writerow([price_val])

