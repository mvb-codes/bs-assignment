# Selenium BrowserStack Assignment

This project is a Python-based automation suite that uses Selenium WebDriver to perform web-based UI testing on the El País website. The tests are configured to run on BrowserStack infrastructure.

## Cloning the Repository

```bash
git clone https://github.com/mvb-codes/bs-assignment.git
cd bs-assignment
```

## Setting up the Environment

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your BrowserStack credentials:

```
BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_access_key
```

## Running the Tests

To run the full test suite:

```bash
browserstack-sdk tests/test_assignment.py
```

## Test Cases Explained

- `test_homepage_load`:
  Ensures that the homepage loads successfully.

- `test_navigate_to_opinion_section_from_homepage`:
  Simulates user navigation from the homepage to the Opinión section and verifies the action.

- `test_fetch_opinion_titles`:
  Fetches all article titles from the Opinión section and logs them.

- `test_word_frequency_count`:
  Downloads the content of the Opinión articles, extracts text, and calculates the frequency of repeated words across articles.

### Title and content printed in both spanish and english will be shown in annotation as info.