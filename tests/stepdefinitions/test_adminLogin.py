import os
import pytest

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

# dotenv_path = Path('D:\Clifford Personal\Projects\learn-indee\.env')
load_dotenv()
url = os.getenv('ADMIN_URL')
acc_name = os.getenv('ACC_THE')
acc_key = os.getenv('KEY_THE')

