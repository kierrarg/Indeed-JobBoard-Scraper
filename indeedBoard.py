import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException

# Set up logging
logging.basicConfig(filename='job_scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Defining qualification
qualifications_keywords = ["C++", "Python", "React", "SQL", "IT", "Unreal Engine", "OOP", "HTML", "CSS", "JavaScript"]

# Initialize the WebDriver
driver = webdriver.Chrome()

# Set the URL of the job search page
url = "https://ca.indeed.com/jobs?q=Junior+Software+Developer&l=Toronto%2C+ON"

# Open the web page
driver.get(url)

# Initialize a variable to keep track of whether there are more pages to scrape
more_pages = True

while more_pages:
    try:
        # Locate job posting elements
        job_postings = driver.find_elements(By.CSS_SELECTOR, ".slider_item")

        for job_posting in job_postings:
            try:
                # Extract job details from the job posting element
                title = job_posting.find_element(By.CSS_SELECTOR, ".jobTitle").text
                company = job_posting.find_element(By.CSS_SELECTOR, ".companyName").text
                location = job_posting.find_element(By.CSS_SELECTOR, ".companyLocation").text
                job_link = job_posting.find_element(By.CSS_SELECTOR, ".jobTitle a").get_attribute("href")

                # Click on the job posting link to go to the job details page
                driver.get(job_link)
                time.sleep(2)  # Wait for the page to load

                # Extract job description from the job details page
                job_description = driver.find_element(By.CSS_SELECTOR, ".jobsearch-jobDescriptionText").text

                # Check if the job description contains your qualifications
                if any(keyword.lower() in job_description.lower() for keyword in qualifications_keywords):
                    # Log the job details
                    logging.info(f"Title: {title}")
                    logging.info(f"Company: {company}")
                    logging.info(f"Location: {location}")
                    logging.info(f"Job Link: {job_link}")

                else:
                    logging.info(f"Skipped job: {title} - Does not match qualifications")

                # Go back to the search results page
                driver.back()
                time.sleep(2)  # Wait for the page to load

            except NoSuchElementException:
                # Handle the "verify you are human" popup by clicking the "back" button
                driver.back()
                logging.warning("Encountered 'verify you are human' popup. Clicked 'back' button.")
                time.sleep(3)  # Wait for the page to load

            except StaleElementReferenceException:
                # Handle stale element reference exception by continuing to the next job posting
                logging.warning("Stale element reference. Continuing to the next job posting.")
                continue

            except Exception as e:
                logging.error(f"Error: {e}")

        # Scroll to the "Next" button and click it
        try:
            # Wait for the "Next" button to be both visible and clickable
            nextButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-testid='pagination-page-next']")))

            # Scroll to the "Next" button to make it clickable
            driver.execute_script("arguments[0].scrollIntoView();", nextButton)

            # Click the "Next" button
            nextButton.click()
            logging.info("Clicked 'Next' button successfully")

        except TimeoutException:
            logging.info("No more pages to navigate.")
            more_pages = False  # Set the flag to indicate no more pages

        except Exception as e:
            logging.warning(f"Error clicking next: {e}")
            more_pages = False  # Set the flag to indicate no more pages

    except NoSuchElementException:
        # Handle the "verify you are human" popup by clicking the "back" button
        driver.back()
        logging.warning("Encountered 'verify you are human' popup. Clicked 'back' button.")
        time.sleep(3)  # Wait for the page to load

    except Exception as e:
        logging.error(f"Error: {e}")

# Close the driver
driver.quit()