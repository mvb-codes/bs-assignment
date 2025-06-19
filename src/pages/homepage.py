from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils import retry_click, annotate

class HomePage:
    # locators
    HOMEPAGE_BODY = (By.TAG_NAME, "body")
    COOKIE_POPUP = (By.ID, "didomi-notice-agree-button")
    HTML_TAG = (By.TAG_NAME, "html")

    def __init__(self, driver):
        self.driver = driver
        self.url = "https://elpais.com/"
        self.wait = WebDriverWait(driver, 10)

    def open(self, max_retries=3):
        """Open the homepage with retry logic"""
        for attempt in range(max_retries):
            try:
                self.driver.get(self.url)
                self.wait.until(EC.presence_of_element_located(self.HOMEPAGE_BODY))
                return "elpais" in self.driver.current_url
            except Exception as e:
                if attempt < max_retries - 1:
                    annotate(self.driver,f"Attempt {attempt + 1} to open homepage.")
                else:
                    annotate(self.driver, f"Failed to open homepage: {e}", "error")
                    return False

    def handle_cookie_popup(self):
        """Click the cookie consent popup if present"""
        try:
            return retry_click(self.driver, *self.COOKIE_POPUP, retries=3, wait_time=5)
        except Exception as e:
            annotate(self.driver, f"Cookie popup not handled: {e}", "error")
            return False

    def validate_language(self, expected_lang="es-ES"):
        """Check if <html lang="..."> matches expected language"""
        try:
            html = self.driver.find_element(*self.HTML_TAG)
            return html.get_attribute("lang") == expected_lang
        except Exception as e:
            annotate(self.driver,f"Could not validate language: {e}", "error")
            return False
