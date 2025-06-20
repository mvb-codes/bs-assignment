import os
import requests
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.utils import translate_text, annotate

class OpinionPage:
    # Locators
    OPINION_LINK = (By.CSS_SELECTOR, "a[href*='/opinion']")
    ARTICLE = (By.CSS_SELECTOR, "article")
    HEADER = (By.TAG_NAME, "h2")
    PARAGRAPH = (By.TAG_NAME, "p")
    IMAGE = (By.TAG_NAME, "img")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def go_to_opinion_section(self):
        try:
            # Open mobile hamburger menu if present
            try:
                hamburger = self.driver.find_element(By.ID, "btn_open_hamburger")
                hamburger.click()
                time.sleep(1)  # Allow menu to slide in
            except:
                pass

            # Locate the Opinión link by href
            opinion_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="https://elpais.com/opinion/"]'))
            )

            # Scroll and force click via JS to avoid interception
            self.driver.execute_script("arguments[0].scrollIntoView(true);", opinion_link)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", opinion_link)

            return True

        except Exception as e:
            annotate(self.driver, f"Could not go to Opinión: {e}", "error")
            return False

    def scrape_articles(self, num_articles=5):
        """Scrape titles, content, and images from top opinion articles"""
        try:
            self.wait.until(EC.presence_of_all_elements_located(self.ARTICLE))
            articles = self.driver.find_elements(*self.ARTICLE)[:num_articles]
            if not articles:
                annotate(self.driver, "No articles found", "warn")
                return []

            os.makedirs("images", exist_ok=True)
            translated_titles = []

            for i, article in enumerate(articles):
                try:
                    title_el = article.find_element(*self.HEADER)
                    title = title_el.text.strip()
                    if not title:
                        continue

                    content_el = article.find_elements(*self.PARAGRAPH)
                    content = content_el[0].text.strip() if content_el else "No content available."

                    translated = translate_text(title)
                    if not translated:
                        continue

                    translated_titles.append(translated)

                    img_el = article.find_elements(*self.IMAGE)
                    if img_el:
                        img_url = img_el[0].get_attribute("src")
                        if img_url:
                            response = requests.get(img_url)
                            if response.status_code == 200:
                                with open(f"images/article_{i + 1}.jpg", "wb") as f:
                                    f.write(response.content)

                    annotate(self.driver, f"\n[Article {i + 1}]\n"
                        f"Title (ES): {title}\n"
                        f"Title (EN): {translated}\n"
                        f"Content: {content[:200]}...\n"
                        f"{'Image saved' if img_el else 'No image found'}")

                except Exception as e:
                    annotate(self.driver,f"Article {i + 1} failed: {e}", "failed")

            return translated_titles

        except Exception as e:
            annotate(self.driver,f"Scraping failed: {e}", "error")
            return []
