from configparser import ConfigParser

def readConfig(section, option):
    config = ConfigParser()
    config.read("configData.ini")
    return config.get(section, option)