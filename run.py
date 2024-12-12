import requests
from bs4 import BeautifulSoup
import json
import os
import smtplib
from apscheduler.schedulers.blocking import BlockingScheduler

term = os.environ.get('SEARCHTERM', "b580")
sleep = os.environ.get('SLEEP', 0.084)

if not os.path.exists(os.getcwd()+'/json'):
    os.mkdir(os.getcwd()+'/json')

backup = os.getcwd()+'/json'
os.chdir(backup)

def neweggButton():
    r = requests.get('https://www.newegg.com/p/N82E16814883006')

    soup = BeautifulSoup(r.content, 'html.parser')

    s = soup.find('button', class_='btn')

    print(s.get_text())

def neweggPage():
    try:
        r = requests.get('https://www.newegg.com/p/pl?d='+term)
        print("Success: Website read")
    except Exception as e:
        print("Error: " + e.message)

    soup = BeautifulSoup(r.content, 'html.parser')

    itemNames = soup.find_all('a', class_='item-title')
    itemPrices = soup.find_all('div', class_='item-button-area')
    filteredNames = [string for string in itemNames if "B580" in string.get_text()]

    itemsDict = neweggCreateDict(filteredNames, itemPrices)

    compare(itemsDict, 'newegg.json')

    jsonObj = json.dumps(itemsDict, indent=4)
    try:
        with open("newegg.json", "w") as outFile:
            outFile.write(jsonObj)
        print("Success: File written")
    except Exception as e:
        print("Error: " + e.message)


def compare(newData, file):
    try:
        if os.path.isfile(backup+'/'+file):
            with open(file, 'r') as f:
                oldData = json.load(f)
            for item in newData:
                if newData[item] != oldData[item]:
                    emailChange(item+' Status Changed')
    except Exception as e:
        print("Error: " + e.message)

def neweggCreateDict(names, prices):
    elements = len(names)
    thisDict = {}
    for i in range(elements):
        thisDict[names[i].get_text()] = prices[i].get_text()
    
    return thisDict

def emailChange(text):
    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login('jzshaw13@gmail.com', 'ikgn jyfk igms wvid')
        smtp_server.sendmail('jzshaw13@gmail.com', 'jzshaw18@gmail.com', text)
        smtp_server.quit()
        print('Email sent successfully')
    except Exception as e:
        print("Error: " + e.message)


neweggPage()
scheduler = BlockingScheduler()
scheduler.add_job(neweggPage,'interval', hours=sleep)
scheduler.start()