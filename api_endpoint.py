# filename: api_endpoint.py

from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')

# Initialize FastAPI app
app = FastAPI()

# Configure Selenium to use the ChromeDriver in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Specify the path to the ChromeDriver
chrome_driver_path = "/usr/local/bin/chromedriver"

# Initialize the Service object with the path to the ChromeDriver
service = Service(chrome_driver_path)

# Initialize the browser instance
browser = webdriver.Chrome(service=service, options=chrome_options)


@app.on_event("startup")
async def startup_event():
    pass


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
    try:
        browser.get(f"https://twitter.com/{TWITTER_USERNAME}")
        time.sleep(3)

        # XPath to locate the username input field
        username_xpath = "//div[@class='css-175oi2r r-18u37iz r-1pi2tsx r-1wtj0ep r-u8s1d r-13qz1uu']/div/input"
        # Wait until the username field is present
        username_field = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, username_xpath)))


        # Find the username field and input the username
        username_field = browser.find_element(By.NAME, "session[username_or_email]")

        username_field.send_keys(TWITTER_USERNAME)

        # Click on the "Next" button, if present
        try:
            next_button = browser.find_element(By.XPATH, "//span[text()='Next']")
            next_button.click()
            time.sleep(3)
        except Exception:
            pass  # "Next" button may not be visible or necessary

        # Find the password field and input the password
        password_field = browser.find_element(By.NAME, "session[password]")
        password_field.send_keys(TWITTER_PASSWORD)
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)

        # After login, check if we are on the home page
        if "home" not in browser.current_url:
            raise HTTPException(status_code=401, detail="Login failed")
        return {"message": "Login successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


@app.get("/read_profile")
async def read_profile():
    return {"message": "Read profile functionality to be implemented"}


@app.get("/read_posts")
async def read_posts():
    return {"message": "Read posts functionality to be implemented"}


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
