import requests
from bs4 import BeautifulSoup
import json

def neweggButton():
    r = requests.get('https://www.newegg.com/p/N82E16814883006')

    soup = BeautifulSoup(r.content, 'html.parser')

    s = soup.find('button', class_='btn')

    print(s.get_text())

def neweggPage():
    r = requests.get('https://www.newegg.com/p/pl?d=b580')

    soup = BeautifulSoup(r.content, 'html.parser')

    itemNames = soup.find_all('a', class_='item-title')
    itemPrices = soup.find_all('div', class_='item-button-area')
    filteredNames = [string for string in itemNames if "B580" in string.get_text()]

    neweggJson(filteredNames, itemPrices)


#def compare():

def neweggJson(names, prices):

    elements = len(names)
    thisDict = {}
    for i in range(elements):
        thisDict[names[i].get_text()] = prices[i].get_text()
    
    thisJson = json.dumps(thisDict)

    print(thisJson)




neweggPage()