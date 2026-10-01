from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = "index.htm"

    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[value='Log In']")

    def load(self):
        return self.open(self.PATH)

    def login(self, username, password):
        self._type(self.USERNAME, username)
        self._type(self.PASSWORD, password)
        self._click(self.LOGIN_BUTTON)
        return self
