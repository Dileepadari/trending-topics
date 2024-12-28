from seleniumwire.undetected_chromedriver.v2 import Chrome, ChromeOptions
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytz
from datetime import datetime
import uuid
from db import get_db
from config import TWITTER_URL, TWITTER_USERNAME, TWITTER_PASSWORD, TWITTER_MAIL, PROXY_URI

ist = pytz.timezone('Asia/Kolkata')
chromedriver_autoinstaller.install()

def setup_driver():
    options = ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    sel_options = {
        'proxy': {
            'http': PROXY_URI,
            'https': PROXY_URI,
        }
    }
    return Chrome(options=options, seleniumwire_options=sel_options)

def login_to_twitter(driver):
    driver.get(TWITTER_URL)
    time.sleep(3)
    try:
        username_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, 'text'))  # Or try a different XPath if necessary
        )

        username_input.send_keys(TWITTER_USERNAME)
        username_input.send_keys(Keys.RETURN)
    except:
        print("Username input not found")

    try:
        password_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, 'password'))
        )

        password_input.send_keys(TWITTER_PASSWORD)
        password_input.send_keys(Keys.RETURN)
    except:
        confim_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, 'text'))
        )
        confim_input.send_keys(TWITTER_MAIL)
        confim_input.send_keys(Keys.RETURN)

        password_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, 'password'))
        )

        password_input.send_keys(TWITTER_PASSWORD)
        password_input.send_keys(Keys.RETURN)

        try:
            confim_input = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.NAME, 'text'))
            )
            confim_input.send_keys(TWITTER_MAIL)
            confim_input.send_keys(Keys.RETURN)
        except:
            print("Confirmation input not needed")


def scrape_trending_topics():
    driver = setup_driver()
    try:
        login_to_twitter(driver)
        time.sleep(3)
        driver.get("https://x.com/explore/tabs/trending")
        time.sleep(2)
        trending_topics = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@aria-label='Timeline: Explore']//div[contains(@data-testid, 'trend')]"))
        )
        trends = [topic.text for topic in trending_topics]

        driver.get("https://httpbin.org/ip")
        ip = driver.find_element(By.TAG_NAME, "body").text
        data = save_to_mongo(trends, ip)
        return data
    finally:
        driver.quit()

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
        "timestamp": datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S"),
        "ip_address": ip,
    }
    collection.insert_one(data)
    return data
