import pytest

from pages.accounts_page import AccountsOverviewPage
from pages.login_page import LoginPage


@pytest.mark.tc_id("TC-LOG-01")
def test_login_with_valid_credentials(driver, registered_user):
    LoginPage(driver).load().login(registered_user.username, registered_user.password)
    assert AccountsOverviewPage(driver).is_loaded(), "Accounts Overview not shown after login"


@pytest.mark.tc_id("TC-LOG-02")
def test_login_with_wrong_password_is_rejected(driver, registered_user):
    page = LoginPage(driver).load().login(registered_user.username, "WrongPassword!1")
    assert "could not be verified" in page.error_text()


@pytest.mark.tc_id("TC-LOG-03")
def test_login_with_unknown_username_is_rejected(driver):
    page = LoginPage(driver).load().login("no_such_user_zz91", "Password123!")
    assert "could not be verified" in page.error_text()


@pytest.mark.tc_id("TC-LOG-04")
def test_login_with_empty_credentials_is_rejected(driver):
    page = LoginPage(driver).load().login("", "")
    assert "enter a username and password" in page.error_text().lower()
