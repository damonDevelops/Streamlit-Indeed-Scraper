import streamlit as st
import pandas as pd
from job_scraper_utils import *
from streamlit_extras.buy_me_a_coffee import button

# Pre-defined list of countries with URLs
COUNTRY_URLS = {
    "Nigeria": 'https://ng.indeed.com',
    "United Kingdom": 'https://uk.indeed.com',
    "United States": 'https://www.indeed.com',
    "Canada": 'https://ca.indeed.com',
    "Germany": 'https://de.indeed.com',
    "Australia": 'https://au.indeed.com',
    "South Africa": 'https://za.indeed.com',
    "Sweden": 'https://se.indeed.com',
    "Singapore": 'https://www.indeed.com.sg',
    "Switzerland": 'https://www.indeed.ch',
    "United Arab Emirates": 'https://www.indeed.ae',
    "New Zealand": 'https://nz.indeed.com',
    "India": 'https://www.indeed.co.in',
    "France": 'https://www.indeed.fr',
    "Italy": 'https://it.indeed.com',
    "Spain": 'https://www.indeed.es',
    "Japan": 'https://jp.indeed.com',
    "South Korea": 'https://kr.indeed.com',
    "Brazil": 'https://www.indeed.com.br',
    "Mexico": 'https://www.indeed.com.mx',
    "China": 'https://cn.indeed.com',
    "Saudi Arabia": 'https://sa.indeed.com',
    "Egypt": 'https://eg.indeed.com',
    "Thailand": 'https://th.indeed.com',
    "Vietnam": 'https://vn.indeed.com',
    "Argentina": 'https://ar.indeed.com',
    "Ireland": 'https://ie.indeed.com'
}

# Streamlit page setup
st.set_page_config(page_title="Indeed Job Scraper", layout="wide")

st.markdown("# 📈 Indeed Job Scraper by [@DamonDevelops](https://damon-develops.tech)")

button(username="damonDevelops", floating=False, width=300, font="Poppins")

st.markdown("""
This tool allows you to input your job search parameters and download the results in a CSV file to quickly review job postings.
""")

def main():
    st.markdown(
        "This scraper runs **locally** on your machine. Use the interface below to input job search parameters."
    )

    # User input form
    with st.form("job_search_form"):
        country = st.selectbox("Select Country", options=list(COUNTRY_URLS.keys()), index=0)
        job_position = st.text_input("Enter Job Title", value="Software Engineer")
        job_location = st.text_input("Enter Job Location", value="Sydney")
        date_posted = st.slider("Days Since Job Posted", min_value=1, max_value=30, value=7)
        max_jobs = st.slider("Max Jobs to Scrape", min_value=1, max_value=100, value=50)

        submit_button = st.form_submit_button("Start Scraping")

    if submit_button:
        country_url = COUNTRY_URLS[country]

        # Start scraping on the user's machine
        st.info("Starting job scraping on your machine... Please wait.")
        driver = configure_webdriver()  # This will run locally

        try:
            full_url = search_jobs(driver, country_url, job_position, job_location, date_posted)
            df = scrape_job_data(driver, country_url, max_jobs)

            if df.empty:
                st.warning("No jobs found for the given criteria.")
            else:
                st.success(f"Scraped {len(df)} jobs successfully!")
                st.dataframe(df)

                # Provide CSV download link
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"{job_position}_{job_location}.csv",
                    mime="text/csv",
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")

        finally:
            driver.quit()

if __name__ == "__main__":
    main()