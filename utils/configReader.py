import pathlib
from configparser import ConfigParser

def readConfig(section, option):
    config = ConfigParser()
    ini_path = pathlib.Path(__file__).parent / "configData.ini"
    config.read(ini_path)
    return config.get(section, option)