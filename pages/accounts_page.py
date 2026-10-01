from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class AccountsOverviewPage(BasePage):
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href*='logout']")

    def is_loaded(self):
        """Logged-in state: the Accounts Overview heading and a Log Out link are shown."""
        from selenium.common.exceptions import TimeoutException
        try:
            self.wait.until(EC.visibility_of_element_located(self.LOGOUT_LINK))
        except TimeoutException:
            return False
        return self.panel_contains("Accounts Overview")
