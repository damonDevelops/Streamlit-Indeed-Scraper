import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import re

def configure_webdriver():
    """Configure the Selenium WebDriver with stealth settings."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    stealth(driver, languages=["en-US", "en"], vendor="Google Inc.",
            platform="Win32", webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True)
    return driver

def search_jobs(driver, country, job_position, job_location, date_posted):
    """Search for jobs on Indeed and return the search URL."""
    url = f'{country}/jobs?q={"+".join(job_position.split())}&l={job_location}&fromage={date_posted}'
    print(f"Search URL: {url}")
    driver.get(url)
    return url

def scrape_job_data(driver, country, max_jobs):
    """Scrape job data from the Indeed search results with a job limit."""
    df = pd.DataFrame(columns=['Link', 'Job Title', 'Company', 'Date Posted', 'Location'])
    job_count = 0

    while job_count < max_jobs:
        soup = BeautifulSoup(driver.page_source, 'lxml')
        boxes = soup.find_all('div', class_='job_seen_beacon')

        for box in boxes:
            if job_count >= max_jobs:
                break

            try:
                # Extract job details
                link_tag = box.find('a', href=True)
                link = link_tag['href'] if link_tag else ''
                link_full = country + link

                job_title_tag = box.find('a', class_=re.compile(r'jcs-JobTitle css-.*'))
                job_title = job_title_tag.text.strip() if job_title_tag else 'N/A'

                company_tag = box.find('span', {'data-testid': 'company-name'})
                company = company_tag.text.strip() if company_tag else 'N/A'

                date_posted = box.find('span', class_='date').text.strip() if box.find('span', class_='date') else 'N/A'
                location = box.find('div', {'data-testid': 'text-location'}).get_text(strip=True) if box.find('div', {'data-testid': 'text-location'}) else 'N/A'

                # Add data to DataFrame
                new_data = pd.DataFrame({
                    'Link': [link_full], 'Job Title': [job_title],
                    'Company': [company], 'Date Posted': [date_posted],
                    'Location': [location]
                })
                df = pd.concat([df, new_data], ignore_index=True)
                job_count += 1

            except Exception as e:
                print(f"Error processing job entry: {e}")

        # Handle pagination
        try:
            next_page = soup.find('a', {'aria-label': 'Next Page'})['href']
            driver.get(country + next_page)
        except (AttributeError, TypeError):
            break

    return df
