from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Setup the webdriver (this example uses Chrome)
driver = webdriver.Chrome()

# Navigate to Twitter's main page
driver.get("https://twitter.com/")

# Wait for the page to load
time.sleep(5)

# Try to locate the Log in button
try:
    accept_cookies = driver.find_element(By.XPATH, "//div[contains(@class, 'r-1phboty') and .//span[contains(text(), 'Accept all cookies')]]")
    # accept_cookies = driver.find_element(By.XPATH, "//span[contains(text(), 'Accept all cookies')]]")

    # XPath based on the data-testid attribute
    # a href="/login"
    # login_button = driver.find_element(By.XPATH, '//a[@data-testid="login"]')
    # print("XPath of the Log in button found:", login_button.get_attribute('outerHTML'))
    print("XPath of the Accept cookies  button found:", accept_cookies.get_attribute('outerHTML'))
except Exception as e:
    print("Error finding the Log in button:", e)

# Close the browser
driver.quit()
