import requests
from bs4 import BeautifulSoup
import csv

response = requests.get('https://www.kijiji.ca/b-achat-et-vente/ville-de-montreal/c10l1700281')

soup = BeautifulSoup(response.text, 'html.parser')
#  soup = BeautifulSoup(response.text, "lxml").text

rentPrice = soup.find_all('div', 'price')

print(rentPrice)
div_tag = rentPrice.div.extract()

print(div_tag)

with open('price.csv', 'wb') as csvfile:
   priceWriter = csv.writer(csvfile, delimiter=' ')

   priceWriter.writerows(rentPrice)
