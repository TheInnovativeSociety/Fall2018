# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 13:18:44 2018

@author: Jan
"""

import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://montreal.craigslist.ca/d/apts-housing-for-rent/search/apa?lang=en&cc=us'

#opening up connection, grabs the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#html parsing
page_soup = soup(page_html, "html.parser")

#grabs each apartment
containers = page_soup.findAll("li", {"class":"result-row"})

filename = "apartments.csv"
f = open(filename, "w")

headers = "title\n"

f.write(headers)

for container in containers:
    
    title_container = container.findAll("a", {"class":"result-title hdrlnk"})
    title = title_container[0].text
    
    #**was able to print out the titles of the post currently working on 
    #printing out the prices
    
   #price_container = container.findAll("span", {"class":"result-price"})
   #price = price_container[0].text
    
    print("title: " + title)
    #print("price: " + price)
    
    f.write(title + "\n")
    #f.write(title + "," +  price + "\n")
    
f.close()    