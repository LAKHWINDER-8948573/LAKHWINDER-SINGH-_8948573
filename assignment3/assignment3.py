import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By  # Import the By class for element locators
import pandas as pd
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open LinkedIn
driver.get("https://www.linkedin.com/login")

# Replace 'your_email' and 'your_password' with your LinkedIn login credentials
email = 'your_email'
password = 'your_password'

# Find and populate the email and password fields, then submit the login form
email_field = driver.find_element(By.ID, "username")
email_field.send_keys(email)
password_field = driver.find_element(By.ID, "password")
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)

# Wait for the page to load
time.sleep(2)

# Create a function to scrape job listings
def scrape_jobs(job_title, location):
    job_data = []

    for page in range(1, 13):  # Scrape up to 12 pages (300 jobs)
        driver.get(f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={location}&start={page * 25}")

        # Scroll down to load more job listings
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for job listings to load
        time.sleep(2)

        # Extract job listings
        job_cards = driver.find_elements(By.CLASS_NAME, "result-card")

        for job_card in job_cards:
            company = job_card.find_element(By.CLASS_NAME, "result-card__subtitle").text.strip()
            job_title = job_card.find_element(By.CLASS_NAME, "result-card__title").text.strip()
            location = job_card.find_element(By.CLASS_NAME, "job-result-card__location").text.strip()
            job_link = job_card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

            job_data.append({
                "company": company,
                "job_title": job_title,
                "location": location,
                "job_link": job_link
            })

    # Create a DataFrame and save it to a CSV file
    df = pd.DataFrame(job_data)
    filename = f"{job_title}_{location}_jobs.csv"
    df.to_csv(filename, index=False, encoding='utf-8')

# Get user input for job title and location
job_title = input("Enter the job title: ")
location = input("Enter the location: ")

# Call the scrape_jobs function
scrape_jobs(job_title, location)

# Close the WebDriver
driver.quit()
