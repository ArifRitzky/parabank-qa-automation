import pytest

from pages.register_page import RegisterPage
from pages.user_data import UserData


@pytest.mark.tc_id("TC-REG-01")
def test_register_with_valid_data(driver):
    """A new customer can register and is logged in automatically."""
    page = RegisterPage(driver).register(UserData.unique())
    assert page.is_registered(), "Success message not shown after valid registration"


@pytest.mark.tc_id("TC-REG-02")
def test_register_with_empty_form_shows_required_errors(driver):
    """Submitting an empty form lists every mandatory field."""
    page = RegisterPage(driver).load().submit()
    errors = page.error_text()
    for expected in (
        "First name is required",
        "Last name is required",
        "Address is required",
        "City is required",
        "State is required",
        "Zip Code is required",
        "Social Security Number is required",
        "Username is required",
        "Password is required",
    ):
        assert expected in errors, f"Missing validation message: {expected!r}"


@pytest.mark.tc_id("TC-REG-03")
def test_register_with_mismatched_passwords_is_rejected(driver):
    page = RegisterPage(driver).register(UserData.unique(), confirm_password="Different123!")
    assert "Passwords did not match" in page.error_text()
    assert not page.panel_contains(RegisterPage.SUCCESS_TEXT)


@pytest.mark.tc_id("TC-REG-04")
def test_register_with_existing_username_is_rejected(driver):
    user = UserData.unique()
    assert RegisterPage(driver).register(user).is_registered(), "Setup: first registration failed"

    driver.delete_all_cookies()  # log out of the new session, then try to reuse the username
    page = RegisterPage(driver).register(user)
    assert "username already exists" in page.error_text().lower()
