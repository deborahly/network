"""
# Filename: run_selenium.py
"""

## Run selenium and chrome driver to scrape data from cloudbytes.dev
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase


# Create your tests here.
class Test1(LiveServerTestCase):
    def test_all_post_pages_should_exist(self):

        ## Setup chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless") # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")

        # Set path to chromedriver as per your configuration
        webdriver_service = Service("/home/deborahly/chromedriver/stable/chromedriver")

        # Choose Chrome Browser
        selenium= webdriver.Chrome(service=webdriver_service, options=chrome_options)

        #Choose your url to visit
        selenium.get('http://127.0.0.1:8000/')

        # Extract element from page
        title = browser.find_element(by=By.XPATH, value='//*[@id="posts"]/h3')
        
        # Check result
        assert title.text == "Ally posts"

        #Wait for 10 seconds
        time.sleep(2)
        selenium.quit()



