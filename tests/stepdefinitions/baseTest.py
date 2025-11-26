import pytest

from tests.conftest import failure_screenshot  # noqa: F401
from tests.conftest import get_browser


# empty base class to blanket all the fixtures (optimization)
@pytest.mark.usefixtures("failure_screenshot", "get_browser")
class BaseTest:
    browser = get_browser
