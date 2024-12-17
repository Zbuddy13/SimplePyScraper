import requests
from bs4 import BeautifulSoup
import json
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv
import shutil
import modules.config as config
import websites.newegg as n

# YAML based config
# Gives the location of the YAML Configuration File
#location = os.environ.get("config", "config.yaml")
# Import config and print
conf = config.importConfig(os.getcwd()+"/config.yaml")
print(json.dumps(conf, indent=4))
# Import arguments
args = conf["args"]

# Env based config
# if os.path.isfile(os.getcwd()+"/.env"):
#     load_dotenv()
# term = os.environ.get('SEARCH_TERM', "")
# sleep = os.environ.get('SLEEP', 5)
# jsonFile = os.environ.get('FILE_NAME', '')
# fromAddress = os.environ.get('FROM_EMAIL', '')
# toAddress = os.environ.get('TO_EMAIL', '')
# emailAppPassword = os.environ.get('APP_PASSWORD', '')
# os.environ['TZ'] = 'America/New_York'
# print(f"Starting variables set to: \n SEARCH_TERM={term} \n SLEEP={int(sleep)} \n FILE_NAME={jsonFile} \n FROM={fromAddress} \n TO={toAddress} \n PASSWORD={emailAppPassword}")

# Set or create the path to hold the json
if os.path.exists(os.getcwd()+'/json'):
    try:
        shutil.rmtree(os.getcwd()+'/json')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
os.mkdir(os.getcwd()+'/json')
backup = os.getcwd()+'/json'
os.chdir(backup)

# add case that if there is a new entry
# if the size of the new and old are different find the new entry and email
def compare(newData, file):
    try:
        if os.path.isfile(backup+'/'+file):
            with open(file, 'r') as f:
                oldData = json.load(f)
            for item in newData: # add else case for new or removed listing(item removed)
                if item in oldData:
                    if newData[item][0] != oldData[item][0]:
                        #emailChange(item+' Status Changed to '+ newData[item][0], " Link: " + newData[item][1])
                        print(item+' Status Changed to '+ newData[item][0] + "Link " + newData[item][1])
                else:
                    if(len(newData) > len(oldData)):
                        emailChange('New Item Added '+item+' Status '+ newData[item][0], " Link: " + newData[item][1])
    except Exception as e:
        print("Error: " + e.message)

if __name__ == "__main__":
    # scheduler = BlockingScheduler()
    # scheduler.add_job(neweggPage,'interval', minutes=int(sleep))
    # scheduler.start()
    for key in conf["websites"]["newegg"]["in-stock"]:
        print(key)
        items = n.neweggPage(key)
        print(items)
        compare(items, "newegg_items.json")

        jsonObj = json.dumps(items, indent=4)
        try:
            with open("newegg_items.json", "w") as outFile:
                outFile.write(jsonObj)
            print("Success: File written")
        except Exception as e:
            print("Error: " + e.message)