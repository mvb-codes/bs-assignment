import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

from src.pages.homepage import HomePage
from src.pages.opinionpage import OpinionPage
from src.utils import count_repeated_words, annotate

load_dotenv()

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.set_capability('sessionName', 'Assignment')
    driver = webdriver.Remote(
    command_executor='https://hub.browserstack.com/wd/hub',
    options=options
)
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def setup_pages(driver):
    home = HomePage(driver)
    opinion = OpinionPage(driver)
    return home, opinion


def test_open_homepage_successfully(driver, setup_pages):
    home, _ = setup_pages
    assert home.open(), "Homepage did not load successfully after retries."
    annotate(driver, "Homepage loaded successfully.")


def test_dismiss_cookie_popup_if_present(driver, setup_pages):
    home, _ = setup_pages
    closed = home.handle_cookie_popup()
    if closed:
        annotate(driver, "Cookie popup dismissed.")
    else:
        annotate(driver, "Cookie popup not found or failed to dismiss.", level="warning")


def test_have_language_set_to_spanish(driver, setup_pages):
    home, _ = setup_pages
    assert home.validate_language(), "Language is not set to Spanish (es-ES)."
    annotate(driver, "Page language verified as Spanish (es-ES).")


def test_navigate_to_opinion_section_from_homepage(driver, setup_pages):
    _, opinion = setup_pages
    assert opinion.go_to_opinion_section(), "Could not click 'Opinión' link."
    assert "opinion" in driver.current_url.lower(), "Did not reach the Opinión section URL."
    annotate(driver, "Successfully navigated to Opinión section.")


def test_scrape_and_translate_top_opinion_articles(driver, setup_pages):
    _, opinion = setup_pages
    titles = opinion.scrape_articles(num_articles=5)
    assert titles, "No article titles were scraped."

    top_words = count_repeated_words(titles)
    filtered_words = [(word, freq) for word, freq in top_words if freq > 2]

    annotate(driver, "\nTop Repeated Words in Article Titles (more than 2 occurrences):")
    annotate(driver, "-" * 50)

    if not filtered_words:
        annotate(driver, "No repeated words found above the threshold.")
    else:
        for i, (word, freq) in enumerate(filtered_words, start=1):
            annotate(driver, f"{i:>2}. {word:<15} - {freq} times")

    annotate(driver, "-" * 50)
    annotate(driver, "Articles scraped and processed successfully.")


