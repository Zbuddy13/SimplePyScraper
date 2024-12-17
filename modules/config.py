import os
import yaml

# Reads in the config file
def importConfig(filename):
    with open(filename, 'r') as file:
        try:
            conf = yaml.safe_load(file)
            if conf.get("websites", None):
                for website in conf["websites"]:
                    if not conf["websites"][website].get("in-stock", None):
                        conf["websites"][website]["in-stock"] = 0
                    if not conf["websites"][website].get("price", None):
                        conf["websites"][website]["price"] = 0
            else:
                print("No Websites Provided, exiting...")
            if not conf.get("args", None):
                conf["args"] = {}
            if not conf["args"].get("interval", None):
                conf["args"]["interval"] = 0
            if not conf["args"].get("from_email", None):
                conf["args"]["from_email"] = 0
            if not conf["args"].get("from_password", None):
                conf["args"]["from_password"] = 0
            if not conf["args"].get("to_email", None):
                conf["args"]["to_email"] = 0
            if not conf["args"].get("tz", None):
                conf["args"]["tz"] = 'America/New_York'
            else:
                print("Config read successfully")
            return conf
        except yaml.YAMLError:
            return None