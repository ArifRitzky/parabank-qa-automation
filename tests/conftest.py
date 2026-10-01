import os
import time
from pathlib import Path

import pytest

from pages.user_data import UserData

ROOT = Path(__file__).resolve().parent.parent
SCREENSHOT_DIR = ROOT / "screenshots"


def _new_driver():
    # Imported here so that tooling which only needs the reporting hooks does not need Selenium.
    from selenium import webdriver

    options = webdriver.ChromeOptions()
    if os.getenv("HEADLESS", "0") == "1":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,900")
    return webdriver.Chrome(options=options)


@pytest.fixture
def driver():
    """A fresh browser per test, so no test can leak session state into another."""
    drv = _new_driver()
    yield drv
    drv.quit()


@pytest.fixture(scope="session")
def registered_user():
    """One account registered up front and shared (read-only) by the login tests.

    Login tests therefore do not depend on the registration *test* passing or running first.
    """
    from pages.register_page import RegisterPage

    user = UserData.unique()
    drv = _new_driver()
    try:
        page = RegisterPage(drv).register(user)
        if not page.is_registered():
            pytest.fail(f"Setup failed: could not register user {user.username}")
    finally:
        drv.quit()
    return user


@pytest.fixture(autouse=True)
def _record_tc_id(request, record_property):
    marker = request.node.get_closest_marker("tc_id")
    if marker:
        record_property("tc_id", marker.args[0])


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Save a screenshot when a test fails, and attach its path to the JUnit report."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed and "driver" in item.funcargs:
        SCREENSHOT_DIR.mkdir(exist_ok=True)
        path = SCREENSHOT_DIR / f"{item.name}_{int(time.time())}.png"
        try:
            item.funcargs["driver"].save_screenshot(str(path))
            item.user_properties.append(("screenshot", path.name))
        except Exception:
            pass  # a dead browser must not hide the real failure
