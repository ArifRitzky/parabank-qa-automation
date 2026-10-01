from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class RegisterPage(BasePage):
    PATH = "register.htm"

    FIELDS = {
        "first_name": (By.ID, "customer.firstName"),
        "last_name": (By.ID, "customer.lastName"),
        "street": (By.ID, "customer.address.street"),
        "city": (By.ID, "customer.address.city"),
        "state": (By.ID, "customer.address.state"),
        "zip_code": (By.ID, "customer.address.zipCode"),
        "phone": (By.ID, "customer.phoneNumber"),
        "ssn": (By.ID, "customer.ssn"),
        "username": (By.ID, "customer.username"),
        "password": (By.ID, "customer.password"),
        "confirm": (By.ID, "repeatedPassword"),
    }
    REGISTER_BUTTON = (By.CSS_SELECTOR, "input[value='Register']")
    SUCCESS_TEXT = "Your account was created successfully"

    def load(self):
        return self.open(self.PATH)

    def fill(self, user, confirm_password=None):
        values = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "street": user.street,
            "city": user.city,
            "state": user.state,
            "zip_code": user.zip_code,
            "phone": user.phone,
            "ssn": user.ssn,
            "username": user.username,
            "password": user.password,
            "confirm": user.password if confirm_password is None else confirm_password,
        }
        for name, value in values.items():
            self._type(self.FIELDS[name], value)
        return self

    def submit(self):
        self._click(self.REGISTER_BUTTON)
        return self

    def register(self, user, confirm_password=None):
        return self.load().fill(user, confirm_password).submit()

    def is_registered(self):
        return self.panel_contains(self.SUCCESS_TEXT)
