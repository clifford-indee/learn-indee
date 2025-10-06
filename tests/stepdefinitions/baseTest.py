import pytest
from tests.conftest import get_browser
from tests.conftest import failure_screenshot


# empty base class to blanket all the fixtures (optimization)
@pytest.mark.usefixtures("failure_screenshot", "get_browser")
class BaseTest:
    browser = get_browser