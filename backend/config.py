from seleniumwire.undetected_chromedriver.v2 import Chrome, ChromeOptions
from selenium.webdriver.common.by import By

proxy = 'http://dileepadari:stir_password@us-ca.proxymesh.com:31280'

# Configure Chrome options
chrome_options = ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--headless')  # Optional: Headless mode

# Set proxy options for Selenium Wire
seleniumwire_options = {
    'proxy': {
        'http': proxy,
        'https': proxy,
        'no_proxy': ''  # Disable bypassing proxies for local addresses
    }
}

# Initialize the Chrome driver with Selenium Wire options
driver = Chrome(seleniumwire_options=seleniumwire_options, options=chrome_options)

try:
    driver.get("https://httpbin.org/ip")
    ip = driver.find_element(By.TAG_NAME, "body").text
    print(ip)
finally:
    driver.quit()  # Ensure the driver quits
