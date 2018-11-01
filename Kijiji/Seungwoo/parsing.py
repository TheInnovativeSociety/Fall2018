import requests
from bs4 import BeautifulSoup
import csv
import parser
import re


response = requests.get('https://www.kijiji.ca/b-achat-et-vente/ville-de-montreal/c10l1700281')

soup = BeautifulSoup(response.text, 'lxml')
#  soup = BeautifulSoup(response.text, "lxml").text

rentPrice = soup.find_all('div', 'price')

print (rentPrice[0])

with open('price.csv', 'w', encoding='UTF-8') as csvfile:
   priceWriter = csv.writer(csvfile)
   for row in rentPrice:
       priceWriter.writerow(row)

# div_tag = rentPrice.div.extract()
#
# print(div_tag)
#
# with open('price.csv', 'wb') as csvfile:
#    priceWriter = csv.writer(csvfile, delimiter=' ')
#
#    priceWriter.writerows(rentPrice)
