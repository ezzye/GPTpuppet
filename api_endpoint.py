# filename: api_endpoint.py

from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
from dotenv import load_dotenv
import time
import traceback

# Load environment variables
load_dotenv()

TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')

# Initialize FastAPI app
app = FastAPI()

# Configure Selenium to use the ChromeDriver in headless mode
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Specify the path to the ChromeDriver
chrome_driver_path = "/usr/local/bin/chromedriver"

# Initialize the Service object with the path to the ChromeDriver
service = Service(chrome_driver_path)

# Initialize the browser instance
browser = webdriver.Chrome(service=service, options=chrome_options)


# Alternatively, you can use the Lifespan API directly
@app.on_event("startup")
async def new_startup_event():
    # Your new startup code
    pass  # probably not needed


@app.on_event("shutdown")
async def shutdown_event():
    if browser:
        browser.quit()


@app.get("/")
async def read_root():
    return {"message": "API is running"}


@app.post("/login")
async def login():
    if not TWITTER_USERNAME or not TWITTER_PASSWORD:
        raise HTTPException(status_code=400, detail="Twitter credentials not provided")

    # login_url = "https://twitter.com/login"
    try:
        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor()
        await loop.run_in_executor(executor, lambda: browser.get("https://twitter.com/login"))
    except Exception as e:
        print("Twitter login page not found.")
        print(f"An error occurred: {e}")
        print(f"Traceback: {traceback.format_exc()}")  # You'll need to import traceback at the beginning of your file

    try:
        # XPath to locate the username input field using property autocomplete="username"
        username_xpath = "//input[@name='text' and @autocomplete='username']"

        # Find the element using the XPath
        username_field = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, username_xpath))
        )
        print("XPath of the user name found:", username_field.get_attribute('outerHTML'))

        # Send the username to the input field
        username_field.send_keys(TWITTER_USERNAME)

        # Press Enter to submit the form
        username_field.send_keys(Keys.RETURN)
        time.sleep(3)
    except Exception as e:
        print("Twitter user name not found.")
        print(f"An error occurred: {e}")
        print(f"Traceback: {traceback.format_exc()}")  # You'll need to import traceback at the beginning of your file

    # # Click on the "Next" button, if present
    try:
        # XPath to locate the Next button
        # next_button_xpath = "//span[contains(text(), 'Next')]"
        next_button_xpath = "div[contains(@role, 'button')]//span[contains(text(), 'Next')]"

        # Wait until the Next button is clickable
        next_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, next_button_xpath))
        )

        # Click the Next button
        next_button.click()
    except Exception as e:
        print("Twitter next button not found.  Maybe not needed.")
        print(f"An error occurred: {e}")
        print(f"Traceback: {traceback.format_exc()}")  # You'll need to import traceback at the beginning of your file

    # except (NoSuchElementException, TimeoutException) as e:
    #     print("Next button may not be visible or necessary.")
    # Additional error handling if needed

    # Find and fill in the password
    try:
        password_field = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys(TWITTER_PASSWORD)

        # Find and click the Log In button
        login_button_xpath = "//div[@data-testid='LoginForm_Login_Button']"
        login_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, login_button_xpath))
        )
        login_button.click()
        time.sleep(3)
    except Exception as e:
        print("Twitter password not found.")
        print(f"An error occurred: {e}")
        print(f"Traceback: {traceback.format_exc()}")  # You'll need to import traceback at the beginning of your file

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

    # After login, check if we are on the home page

    # Try to locate the Accept cookie button
    try:
        accept_cookies_xpath = "//span[contains(text(), 'Accept all cookies')]"
        accept_cookies_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, accept_cookies_xpath))
        )
        print("XPath of the Accept cookies button found:", accept_cookies_button.get_attribute('outerHTML'))
        accept_cookies_button.click()
    except Exception as e:
        print("Accept cookies button not found.")
        print(f"An error occurred: {e}")
        print(f"Traceback: {traceback.format_exc()}")  # You'll need to import traceback at the beginning of your file

    if f"twitter.com/home" not in browser.current_url:
        raise HTTPException(status_code=401, detail="Login failed")
    return {"message": "Login successful"}


# Placeholder endpoints for other actions
@app.post("/create_post")
async def create_post():
    return {"message": "Create post functionality to be implemented"}


@app.post("/create_reply")
async def create_reply():
    return {"message": "Create reply functionality to be implemented"}


@app.post("/create_quote")
async def create_quote():
    return {"message": "Create quote functionality to be implemented"}


@app.post("/like_post")
async def like_post():
    return {"message": "Like post functionality to be implemented"}


@app.post("/repost")
async def repost():
    return {"message": "Repost functionality to be implemented"}


@app.get("/read/{twitter_username}")
async def read_posts(twitter_username: str):
    print(f"Twitter Username: {twitter_username}")
    return {"message": f"Read posts for Twitter user: {twitter_username}"}


@app.get("/{twitter_username}/profile")
async def read_profile(twitter_username: str):
    try:
        # Now, use Selenium to find elements and extract data.
        # The selectors are based on your provided classes and could change over time.
        # You might need to update them if Twitter updates its HTML structure.

        # Extract the user description
        user_description_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-testid="UserDescription"]'))
        )
        user_description_html = user_description_element.get_attribute('innerHTML')

        # Extract the other details similarly using the appropriate selectors

        # Construct the JSON response
        profile_data = {
            "Username": f"@{twitter_username}",
            "Name": "Extracted Name",
            "UserDescription": user_description_html,
            # Add other details similarly
        }
        return profile_data
    except TimeoutException:
        raise HTTPException(status_code=404, detail="Profile page did not load in time")
    except NoSuchElementException:
        raise HTTPException(status_code=404, detail="Could not find the profile data")


@app.get("/read/{twitter_username}/verified_followers")
async def read_posts(twitter_username: str):
    print(f"Twitter Username: {twitter_username}")
    return {"message": f"Read posts for Twitter user: {twitter_username}"}


@app.get("/read/{twitter_username}/followers_you_follow")
async def read_posts(twitter_username: str):
    print(f"Twitter Username: {twitter_username}")
    return {"message": f"Read posts for Twitter user: {twitter_username}"}


@app.get("/read/{twitter_username}/followers")
async def read_posts(twitter_username: str):
    print(f"Twitter Username: {twitter_username}")
    return {"message": f"Read posts for Twitter user: {twitter_username}"}


@app.get("/read/{twitter_username}/following")
async def read_posts(twitter_username: str):
    print(f"Twitter Username: {twitter_username}")
    return {"message": f"Read posts for Twitter user: {twitter_username}"}


@app.get("/read/{twitter_username}/likes")
async def read_posts(twitter_username: str):
    print(f"Twitter Username: {twitter_username}")
    return {"message": f"Read posts for Twitter user: {twitter_username}"}


@app.get("/read/{twitter_username}/with_replies")
async def read_posts(twitter_username: str):
    print(f"Twitter Username: {twitter_username}")
    return {"message": f"Read posts for Twitter user: {twitter_username}"}


@app.get("/read/{twitter_username}/media")
async def read_posts(twitter_username: str):
    print(f"Twitter Username: {twitter_username}")
    return {"message": f"Read posts for Twitter user: {twitter_username}"}


@app.get("/read_threads")
async def read_threads():
    return {"message": "Read threads functionality to be implemented"}


@app.put("/update_profile")
async def update_profile():
    return {"message": "Update profile functionality to be implemented"}


@app.post("/follow_user")
async def follow_user():
    return {"message": "Follow user functionality to be implemented"}


@app.get("/list_followers")
async def list_followers():
    return {"message": "List followers functionality to be implemented"}


@app.get("/list_following")
async def list_following():
    return {"message": "List following functionality to be implemented"}


# Run the API using Uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
