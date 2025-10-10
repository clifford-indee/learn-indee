import pathlib
from configparser import ConfigParser

from selenium.webdriver.common.by import By


# reads the .ini file and returns the locator tuple
def read_config(section, option: str, *args: str):
    config = ConfigParser()
    ini_path = pathlib.Path(__file__).parent / "configData.ini"
    config.read(ini_path)
    if option.endswith("_XPATH"):
        return (By.XPATH, config.get(section, option) + args[0])
    elif option.endswith("_CSS"):
        return (By.CSS_SELECTOR, config.get(section, option))
    elif option.endswith("_ID"):
        return (By.ID, config.get(section, option))
    raise ValueError(f"Unknown option: {option}")
