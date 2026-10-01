from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://parabank.parasoft.com/parabank"
DEFAULT_TIMEOUT = 10


class BasePage:
    """Shared helpers. Page classes own their locators; tests never touch Selenium directly."""

    ERROR = (By.CSS_SELECTOR, ".error")

    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, path):
        self.driver.get(f"{BASE_URL}/{path}")
        return self

    def _type(self, locator, text):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def _click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def error_text(self):
        """Wait for validation/error messages and return all of them as one string."""
        self.wait.until(EC.visibility_of_element_located(self.ERROR))
        return " | ".join(e.text for e in self.driver.find_elements(*self.ERROR) if e.text)

    def panel_contains(self, text):
        """True if the main content panel shows `text` within the timeout."""
        from selenium.common.exceptions import TimeoutException
        try:
            self.wait.until(
                lambda d: text in d.find_element(By.ID, "rightPanel").text
            )
            return True
        except TimeoutException:
            return False
