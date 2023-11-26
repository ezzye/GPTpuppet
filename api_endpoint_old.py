# filename: api_endpoint.py

from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
from dotenv import load_dotenv

# http://localhost:8000/openapi.json see this endpoint for swagger documentation

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Configure Selenium to use the ChromeDriver in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument(
    "--no-sandbox")  # This option is often required when running Selenium in a headless environment
chrome_options.add_argument("--disable-dev-shm-usage")  # This can help performance in a headless environment

# Specify the path to the ChromeDriver
chrome_driver_path = "/usr/local/bin/chromedriver"  # Replace with the actual path to your ChromeDriver

# Initialize the Service object with the path to the ChromeDriver
service = Service(chrome_driver_path)

# Initialize the browser instance
browser = webdriver.Chrome(service=service, options=chrome_options)


@app.on_event("startup")
async def startup_event():
    # The browser is already initialized outside of the event
    pass


@app.on_event("shutdown")
async def shutdown_event():
    if browser:
        browser.quit()


@app.get("/")
async def read_root():
    return {"message": "API is running"}


# Placeholder for the login endpoint
@app.post("/login")
async def login():
    # Here you would add the code to perform OAuth2 login using Selenium
    # and environment variables for credentials.
    return {"message": "Login functionality to be implemented"}


# Run the API using Uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
