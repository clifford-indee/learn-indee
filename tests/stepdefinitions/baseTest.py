import pytest
import logging

from tests.conftest import get_browser
from tests.conftest import failure_screenshot
from utils.logGenerator import Logger

# set the current file and log level as INFO
log = Logger(__name__, logging.INFO)

# empty base class to blanket all the fixtures (optimization)
@pytest.mark.usefixtures("failure_screenshot", "get_browser")
class BaseTest:
    browser = get_browser
    # log.logger.info("Browser setup {}".format(browserName))