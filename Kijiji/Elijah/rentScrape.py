#! python3

import bs4
import requests
import os, os.path, csv, pyperclip

os.chdir('C:\\Users\\Dell\\Desktop')
url = pyperclip.paste()  # copy kijiji url from clipboard

outputFile = open('price.csv', 'w', newline='') #create csv file in write mode
outputWriter = csv.writer(outputFile, delimiter=",")

z = 0
while z <= 235:
    res = requests.get(url) #downloads url and checks if there are no errors
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")   #turns to html content

    informationDIV = soup.select('div .info-container') #information we want is in a div called .info-container

    titleList = []      #empty dictionary to store title and rent
    rentList = []
    
    if i not 26:
        for i in range(len(informationDIV)):#loops over how # of results per page and puts data intodictionary
            titles = soup.select('div .info-container > .title > a')
            removeNewline = titles[i].getText()
            titleList.append(removeNewline.replace("\n", ""))
            outputWriter.writerow([titleList[i]])
                    
            rents = soup.select('div .price')
            removeNewline = rents[i].getText()
            rentList.append(removeNewline.replace("\n", "").replace("\xa0",""))
            outputWriter.writerow([rentList[i]])
    else:
        nextpageLink = soup.select('a[title="Suivante"]')[0]
        url = 'http://www.kijiji.ca' + nextpageLink.get('href')
        res = requests.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "html.parser")


outputFile.close()
