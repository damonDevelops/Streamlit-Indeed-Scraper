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


def log_page_content(driver, url):
    driver.get(url)
    driver.implicitly_wait(5)
    with open('page_source.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print("Page source logged to 'page_source.html'.")

def search_jobs(driver, country, job_position, job_location, date_posted):
    full_url = f'{country}/jobs?q={"+".join(job_position.split())}&l={job_location}&fromage={date_posted}'
    print("Search URL: " + full_url)
    driver.get(full_url)
    global total_jobs
    try:
        job_count_element = driver.find_element(
            By.XPATH, '//div[starts-with(@class, "jobsearch-JobCountAndSortPane-jobCount")]')
        total_jobs = job_count_element.find_element(By.XPATH, './span').text
        print(f"{total_jobs} found")
    except NoSuchElementException:
        print("No job count found")
        total_jobs = "Unknown"

    driver.save_screenshot('screenshot.png')
    return full_url

def scrape_job_data(driver, country, max_jobs=50):
    """Scrape job data with a limit on the number of jobs."""
    df = pd.DataFrame(columns=['Link', 'Job Title', 'Company', 'Date Posted', 'Location'])
    job_count = 0

    while job_count < max_jobs:
        soup = BeautifulSoup(driver.page_source, 'lxml')
        boxes = soup.find_all('div', class_='job_seen_beacon')

        for box in boxes:
            if job_count >= max_jobs:
                break  # Stop if max job limit is reached

            try:
                # Extract job details
                link_tag = box.find('a', href=True)
                link = link_tag['href'] if link_tag else ''
                link_full = country + link

                job_title_tag = box.find('a', class_=re.compile(r'jcs-JobTitle css-.*'))
                job_title = job_title_tag.text.strip() if job_title_tag else 'N/A'

                company_tag = box.find('span', {'data-testid': 'company-name'})
                company = company_tag.text.strip() if company_tag else 'N/A'

                date_posted = (
                    box.find('span', class_='date').text.strip()
                    if box.find('span', class_='date') else 'N/A'
                )

                location_element = box.find('div', {'data-testid': 'text-location'})
                location = location_element.get_text(strip=True) if location_element else 'N/A'

                # Create a new DataFrame row and append it
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
            next_page_url = country + next_page
            driver.get(next_page_url)
        except (AttributeError, TypeError):
            break  # No more pages

    return df


def clean_data(df):
    def posted(x):
        x = x.replace('PostedPosted', '').strip()
        x = x.replace('EmployerActive', '').strip()
        x = x.replace('PostedToday', '0').strip()
        x = x.replace('PostedJust posted', '0').strip()
        x = x.replace('today', '0').strip()
        return x

    def day(x):
        return x.replace('days ago', '').strip().replace('day ago', '').strip()

    def plus(x):
        return x.replace('+', '').strip()

    df['Date Posted'] = df['Date Posted'].apply(posted).apply(day).apply(plus)
    return df

def sort_data(df):
    def convert_to_integer(x):
        try:
            return int(x)
        except ValueError:
            return float('inf')

    df['Date_num'] = df['Date Posted'].apply(lambda x: x[:2].strip())
    df['Date_num2'] = df['Date_num'].apply(convert_to_integer)
    df.sort_values(by=['Date_num2'], inplace=True)
    return df[['Link', 'Job Title', 'Company', 'Date Posted', 'Location']]


def sort_data(df):
    def convert_to_integer(x):
        try:
            return int(x)
        except ValueError:
            return float('inf')

    df['Date_num'] = df['Date Posted'].apply(lambda x: x[:2].strip())
    df['Date_num2'] = df['Date_num'].apply(convert_to_integer)
    df.sort_values(by=['Date_num2'], inplace=True)
    return df[['Link', 'Job Title', 'Company', 'Date Posted', 'Location']]

def save_csv(df, job_position, job_location):
    """Save the CSV in the same directory where the script is running."""
    # Generate the filename using the job position and location
    filename = f"{job_position}_{job_location}.csv".replace(" ", "_")

    # Save the CSV in the current directory
    file_path = os.path.join(os.getcwd(), filename)  # Use current working directory
    df.to_csv(file_path, index=False)

    print(f"CSV saved at {file_path}.")
    return file_path

def send_email(df, sender_email, receiver_email, job_position, job_location, password):
    msg = MIMEMultipart()
    msg['Subject'] = 'New Jobs from Indeed'
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_email)

    attachment_filename = f"{job_position}_{job_location}.csv"
    csv_content = df.to_csv(index=False).encode()

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(csv_content)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{attachment_filename}"')
    msg.attach(part)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    print("Email sent successfully.")


def send_email_empty(sender, receiver_email, subject, body, password):
    msg = MIMEMultipart()
    password = password

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ','.join(receiver_email)

    # Attach the body as the text/plain part of the email
    msg.attach(MIMEText(body, 'plain'))

    s = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
    s.login(user=sender, password=password)

    s.sendmail(sender, receiver_email, msg.as_string())

    s.quit()


def generate_attachment_filename(job_title, job_location):
    filename = f"{job_title.replace(' ', '_')}_{job_location.replace(' ', '_')}.csv"
    return filename

def handle_csv(df, job_position, job_location, sender_email, receiver_email, password):
    choice = input("Do you want to (1) Save locally or (2) Email the CSV? Enter 1 or 2: ").strip()
    if choice == '1':
        save_csv(df, job_position, job_location)
    elif choice == '2':
        send_email(df, sender_email, receiver_email, job_position, job_location, password)
    else:
        print("Invalid choice. Defaulting to saving locally.")
        save_csv(df, job_position, job_location)