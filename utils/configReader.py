import os
from configparser import ConfigParser

from selenium.webdriver.common.by import By


# reads the .ini file and returns the locator tuple
def read_config(section, option: str, *args: str):
    config = ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), "configData.ini")
    config.read(config_path)
    suffix = args[0] if args else ""
    if option.endswith("_XPATH"):
        return By.XPATH, config.get(section, option) + suffix
    elif option.endswith("_CSS"):
        return By.CSS_SELECTOR, config.get(section, option)
    elif option.endswith("_ID"):
        return By.ID, config.get(section, option)
    raise ValueError(f"Unknown option: {option}")
