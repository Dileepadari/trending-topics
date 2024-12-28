from seleniumwire.undetected_chromedriver.v2 import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time
import uuid
from db import get_db

load_dotenv()

# Configuration
TWITTER_URL = "https://x.com/login"
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")
TWITTER_MAIL = os.getenv("TWITTER_MAIL")
PROXYMESH_URI = os.getenv("PROXY_URI")

# Set up Selenium
def setup_driver():

    options = ChromeOptions()

    options.add_argument('--ignore-certificate-errors')  # Disable SSL certificate validation
    options.add_argument('--incognito')  # Optional: Use incognito mode to avoid caching issues
    # options.add_argument('--headless')  # Optional: Run in headless mode

    sel_options = {
        'proxy': {
            'http': PROXYMESH_URI,
            'https': PROXYMESH_URI,
        }
    }



    # Use the proxy capabilities
    return Chrome(options=options, seleniumwire_options=sel_options)

# Log into Twitter
def login_to_twitter(driver):
    driver.get(TWITTER_URL)
    time.sleep(3)
    try:
        username_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'text'))  # Or try a different XPath if necessary
        )

        username_input.send_keys(TWITTER_USERNAME)
        username_input.send_keys(Keys.RETURN)
    except:
        print("Username input not found")

    try:
        password_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'password'))
        )

        password_input.send_keys(TWITTER_PASSWORD)
        password_input.send_keys(Keys.RETURN)
    except:
        confim_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'text'))
        )
        confim_input.send_keys(TWITTER_MAIL)
        confim_input.send_keys(Keys.RETURN)

        password_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'password'))
        )

        password_input.send_keys(TWITTER_PASSWORD)
        password_input.send_keys(Keys.RETURN)

        try:
            confim_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, 'text'))
            )
            confim_input.send_keys(TWITTER_MAIL)
            confim_input.send_keys(Keys.RETURN)
        except:
            print("Confirmation input not found")


# Save results to MongoDB
def save_to_mongo(trends, ip):
    db = get_db()
    collection = db["trending_topics"]
    data = {
        "_id": str(uuid.uuid4()),
        "nameoftrend1": trends[0] if len(trends) > 0 else None,
        "nameoftrend2": trends[1] if len(trends) > 1 else None,
        "nameoftrend3": trends[2] if len(trends) > 2 else None,
        "nameoftrend4": trends[3] if len(trends) > 3 else None,
        "nameoftrend5": trends[4] if len(trends) > 4 else None,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ip_address": ip,
    }
    collection.insert_one(data)
    return data

# Main Function
def main():
    driver = setup_driver()
    login_to_twitter(driver)
    try:
        # Login and scrape
        time.sleep(3)
        driver.get("https://x.com/explore/tabs/trending")
        time.sleep(2)
        trends = []
        try:
            # Update XPath to target individual trend containers
            trending_topics = WebDriverWait(driver, 50).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//div[@aria-label='Timeline: Explore']//div[contains(@data-testid, 'trend')]")
                )
            )
            # Extract the text for each trend
            trends = [topic.text for topic in trending_topics]
        except Exception as e:
            print("Error extracting trends:", e)



        # Get current IP
        driver.get("https://httpbin.org/ip")
        ip = driver.find_element(By.TAG_NAME, "body").text

        # Save results
        data = save_to_mongo(trends, ip)
        print("Scraped data saved:", data)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
