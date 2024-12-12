import requests
from bs4 import BeautifulSoup
import json
import os
import smtplib
from apscheduler.schedulers.blocking import BlockingScheduler
from email.mime.text import MIMEText
from dotenv import load_dotenv
import shutil

if os.path.isfile(os.getcwd()+"/.env"):
    load_dotenv()

term = os.environ.get('SEARCH_TERM', "")
sleep = os.environ.get('SLEEP', 5)
jsonFile = os.environ.get('FILE_NAME', '')
fromAddress = os.environ.get('FROM_EMAIL', '')
toAddress = os.environ.get('TO_EMAIL', '')
emailAppPassword = os.environ.get('APP_PASSWORD', '')
os.environ['TZ'] = 'America/New_York'

print(f"Starting variables set to: \n SEARCH_TERM={term} \n SLEEP={int(sleep)} \n FILE_NAME={jsonFile} \n FROM={fromAddress} \n TO={toAddress} \n PASSWORD={emailAppPassword}")

if os.path.exists(os.getcwd()+'/json'):
    try:
        shutil.rmtree(os.getcwd()+'/json')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

os.mkdir(os.getcwd()+'/json')
backup = os.getcwd()+'/json'
os.chdir(backup)

def neweggPage():
    try:
        r = requests.get('https://www.newegg.com/p/pl?d='+term)
        print("Success: Website read")
    except Exception as e:
        print("Error: " + e.message)

    soup = BeautifulSoup(r.content, 'html.parser')

    itemNames = soup.find_all('a', class_='item-title')
    itemPrices = soup.find_all('div', class_='item-button-area')
    #itemLinks = soup.find_all('a', class_='item-img', rel_=False)
    for i in itemNames:
        if term.lower() not in i.get_text().lower():
            itemNames.remove(i)
    #print(itemNames[0]['href'])
    #filteredNames = [string for string in itemNames if "B580" in string.get_text()]

    itemsDict = neweggCreateDict(itemNames, itemPrices)

    compare(itemsDict, jsonFile)

    jsonObj = json.dumps(itemsDict, indent=4)
    try:
        with open(jsonFile, "w") as outFile:
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
                if newData[item][0] != oldData[item][0]:
                    emailChange(item+' Status Changed to '+ newData[item][0], " Link: " + newData[item][1])
                    #print(item+' Status Changed to '+ newData[item][0] + "Link " + newData[item][1])
    except Exception as e:
        print("Error: " + e.message)

def neweggCreateDict(names, prices):
    elements = len(names)
    thisDict = {}
    for i in range(elements):
        thisDict[names[i].get_text()] = (prices[i].get_text(),names[i]['href'])
    
    return thisDict

def emailChange(subject, text):
    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(fromAddress, emailAppPassword)
        message = MIMEText(text)
        message['From'] = fromAddress
        message['To'] = toAddress
        message['Subject'] = subject
        smtp_server.sendmail(fromAddress, toAddress, message.as_string())
        smtp_server.quit()
        print('Email sent successfully')
    except Exception as e:
        print("Error: " + e.message)

neweggPage()
scheduler = BlockingScheduler()
scheduler.add_job(neweggPage,'interval', minutes=int(sleep))
scheduler.start()