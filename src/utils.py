import time
import logging as log
from collections import Counter
from googletrans import Translator
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


def retry_click(driver, by, value=None, retries=3, wait_time=3):
    """
    Retry clicking an element that may be flaky or slow to load.
    Can accept (By, value) or unpacked locator tuple.
    """
    if isinstance(by, tuple):
        by, value = by

    for attempt in range(retries):
        try:
            WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((by, value))).click()
            log.info(f"Click succeeded on attempt {attempt + 1}")
            return True
        except Exception as e:
            log.warning(f"Retry click failed (attempt {attempt + 1}): {e}")
            time.sleep(1)

    log.error(f"Failed to click element after {retries} attempts: {by}, {value}")
    return False


def count_repeated_words(titles, top_n=10):
    """
    Return the most common words across all titles.
    """
    log.info(f"Counting top {top_n} repeated words in {len(titles)} titles")
    words = " ".join(titles).lower().split()
    common = Counter(words).most_common(top_n)
    log.debug(f"Top {top_n} words: {common}")
    return common


def translate_text(text, src="es", dest="en"):
    """
    Translate a text from Spanish to English.
    """
    try:
        translator = Translator()
        translated = translator.translate(text, src=src, dest=dest)
        return translated.text
    except Exception as e:
        log.error(f"Translation failed for '{text}': {e}")
        return None


def annotate(driver, message, level="info"):
    """
    Send annotations to BrowserStack session.
    """
    payload = {
        "action": "annotate",
        "arguments": {
            "data": message,
            "level": level
        }
    }
    script = "browserstack_executor: " + json.dumps(payload)
    driver.execute_script(script)
