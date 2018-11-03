#! python3

import bs4
import requests
import os, os.path, csv
from csv import writer
import re

def title_formatter(format_input):
    format_input = format_input.replace("\n", "")
    format_input = format_input.replace(",", " ") 
    format_input = re.sub(r'\s+', ' ', format_input)
    format_input = format_input.replace("\\\\", "\\") 
    format_input = format_input.strip()
    return format_input

def price_formatter(price):
    price = price.replace(",", ".")
    price = re.sub(r'\s+', '', price)
    price = price.replace("$", "")
    return '$' + price.strip()

def address_formatter(address):
    address = address.replace(",", " ")
    address = re.sub(r'\s+', ' ', address)
    return address

def request_bs(url):
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    return soup

url = 'https://www.kijiji.ca/b-appartement-condo/ville-de-montreal/c37l1700281'

# open csv file
file_name = 'kijiji_info.csv'
with open(file_name, 'w+') as output_file:
    csv_writer = writer(output_file, delimiter=',')
    csv_writer.writerow(["Title", "Price", "Address", "Bathroom", "Room", "Furnished", "Pet Allowed"])

soup = request_bs(url)

informationDIV = soup.select('div .info-container')  # information we want is in a div called .info-container
length = len(informationDIV) # to know how many items exist on 1 page.

# On Kijiji, the maximum iterable posts are 2000 
# Even if it shows that there are more posts, it is not recheable 
MAXIMUM = 2000
start = 0
while start < 200:
    number_of_articles = len(soup.select('div .info-container'))
    for i in range(len(informationDIV)):
        start = start + 1
        titles = soup.select('div .info-container > .title > a')

        # getting title
        title = title_formatter(titles[i].getText())

        # checking each element's detail.
        sublink = 'http://www.kijiji.ca' + titles[i].get('href')
        subsoup = request_bs(sublink)
        # please refer to price_formatter function
        price = price_formatter(subsoup.select_one('span[class*="currentPrice"]').text)

        address = address_formatter(subsoup.select_one('span[itemprop="address"]').text)

        child_bathroom = subsoup.find(text=re.compile('Salles de bain')).parent
        bathroom = re.findall('\d+', child_bathroom.parent.select_one('dd').text)[0]

        child_room = subsoup.find(text=re.compile('Chambres')).parent
        room = child_room.parent.select_one('dd').text
        try:
            child_furnished = subsoup.find(text=re.compile('Meublé')).parent
            furnished = child_furnished.parent.select_one('dd').text
        except:
            furnished = 'Unknown'

        try:
            child_animal = subsoup.find(text=re.compile('Animaux acceptés')).parent
            animal = child_animal.parent.select_one('dd').text
        except:
            animal = 'Unknown'

        with open(file_name, "a", encoding='UTF-8') as output_file:
            csv_writer = writer(output_file, delimiter=',')
            csv_writer.writerow([title, price, address, bathroom, room, furnished, animal])
        
    nextpageLink = soup.select('a[title="Suivante"]')[0]
    url = 'http://www.kijiji.ca' + nextpageLink.get('href')
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, "html.parser")

output_file.close()
