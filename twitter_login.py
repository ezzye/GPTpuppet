# filename: twitter_login.py

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

# Retrieve credentials from environment variables
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')

# Initialize the Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


# Function to log into Twitter
def login_to_twitter(username, password):
    try:
        # Open the Twitter login page
        driver.get("https://twitter.com/login")
        time.sleep(3)  # Wait for the page to load

        # Find the username field and enter the username
        username_field = driver.find_element(By.NAME, "session[username_or_email]")
        username_field.send_keys(username)

        # Find the password field and enter the password
        password_field = driver.find_element(By.NAME, "session[password]")
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)  # Press Enter to log in

        time.sleep(5)  # Wait for the login to complete
        print("Login successful")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser
        driver.quit()


# Run the login function with the provided credentials
if __name__ == "__main__":
    if TWITTER_USERNAME and TWITTER_PASSWORD:
        login_to_twitter(TWITTER_USERNAME, TWITTER_PASSWORD)
    else:
        print("Twitter username or password not set in environment variables.")
