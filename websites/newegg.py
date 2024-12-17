import requests
from bs4 import BeautifulSoup
import json
import smtplib

# need to rewrite for selenium
# Returns dict of items
def neweggPage():
    # Pull and parse the website
    try:
        r = requests.get('https://www.newegg.com/p/pl?d=b580')
        print("Success: Website read")
    except Exception as e:
        print("Error: " + e.message)
    soup = BeautifulSoup(r.content, 'html.parser')
    print(soup)
    itemNames = soup.find_all('a', class_='item-title')
    print(itemNames)
    itemPrices = soup.find_all('div', class_='item-button-area')
    print(itemPrices)
    # Remove items that dont match search term
    for i in itemNames:
        if term.lower() not in i.get_text().lower():
            itemNames.remove(i)
    returndict = neweggCreateDict(itemNames, itemPrices)
    print(returndict)
    return returndict

# Create dict of item names and prices
def neweggCreateDict(names, prices):
    elements = len(names)
    thisDict = {}
    for i in range(elements):
        thisDict[names[i].get_text()] = (prices[i].get_text(),names[i]['href'])
    
    return thisDict

# Testing
print(neweggPage())