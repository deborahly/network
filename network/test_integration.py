"""
# Filename: run_self.selenium.py
"""

## Run selenium and chrome driver to scrape data from cloudbytes.dev
from cgi import test
import profile
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Create your tests here.
class IntegrationTestCase(LiveServerTestCase):

    def wait_for_element(self, webdriver, method, query, wait_time=2):
        return WebDriverWait(webdriver, wait_time).until(EC.presence_of_element_located((method, query)))
    
    selenium = None

    def create_driver(self):
        # Setup chrome options
        chrome_options = Options()
        # chrome_options.add_argument("--headless") # Ensure GUI is off
        # chrome_options.add_argument("--no-sandbox")

        # Set path to chromedriver as per your configuration
        webdriver_service = Service("/home/deborahly/chromedriver/stable/chromedriver")

        # Choose Chrome Browser
        return webdriver.Chrome(service=webdriver_service, options=chrome_options)

    def setUp(self) -> None:
        # Choose Chrome Browser
        self.selenium = self.create_driver()
    
    def test_index_page_should_exist(self):
        self.selenium.get("http://127.0.0.1:8000/")
        
        # Check result
        self.assertEqual(self.selenium.title, "Index")

    def test_index_page_1_posts_should_load(self):
        self.selenium.get("http://127.0.0.1:8000/")
        
        self.wait_for_element(self.selenium, By.CLASS_NAME, "card-text")

        # Extract elements from page
        cards = self.selenium.find_elements_by_class_name("card-body")
        card_titles = self.selenium.find_elements_by_class_name("card-title")
        card_subtitles = self.selenium.find_elements_by_class_name("card-subtitle")
        card_texts = self.selenium.find_elements_by_class_name("card-text")

        # Expected result
        expected = 2

        # Check results
        self.assertEqual(len(cards), expected)
        self.assertEqual(len(card_titles), expected)
        self.assertEqual(len(card_subtitles), expected)
        self.assertEqual(len(card_texts), expected)

    def test_index_page_1_likes_should_appear(self):
        self.selenium.get('http://127.0.0.1:8000/')
        self.wait_for_element(self.selenium, By.XPATH, '//*[@id="posts-list"]/div[2]/div/span/span')
        
        # Sets for loop to start at 1
        def nums(first_number, last_number, step = 1):
            return range(first_number, last_number + 1, step)

        # Extract elements from page
        likes_numbers = []

        for i in nums(1,2):
            likes_number = self.selenium.find_element(by=By.XPATH, value=f'//*[@id="posts-list"]/div[{i}]/div/span/span').text
            likes_numbers.append(likes_number)

        # Expected result
        expected = ["0", "1"]
        
        # Check results
        for i in range(1):
            assert likes_numbers[i] == expected[i]

    def test_index_page_1_previous_button_should_be_disabled(self):
        self.selenium.get('http://127.0.0.1:8000/')
        self.wait_for_element(self.selenium, By.XPATH, '//*[@id="previous"]')

        # Extract elements from page
        previous_page = self.selenium.find_element(by=By.XPATH, value='//*[@id="previous"]')
        disabled = previous_page.get_attribute("disabled")

        # Expected result
        expected = "true"

        # Check result
        self.assertEqual(disabled, expected)
    
    def test_index_page_1_next_previous_buttons_work(self):
        self.selenium.get('http://127.0.0.1:8000/')
        self.wait_for_element(self.selenium, By.XPATH, '//*[@id="next"]')

        # Extract elements from page
        next_page = self.selenium.find_element(by=By.XPATH, value='//*[@id="next"]')
        
        # Action
        next_page.click()
        index_page = self.wait_for_element(self.selenium, By.XPATH, "//*[@id='page-index' and @data-page='2']")

        # Expected result for next button
        data_page2 = index_page.get_attribute("data-page")
        expected2 = "2"

        # # Check result for next button
        self.assertEqual(data_page2, expected2)

        # Extract elements from page
        previous_page = self.selenium.find_element(by=By.XPATH, value='//*[@id="previous"]')
        
        # Action
        previous_page.click()
        index_page = self.wait_for_element(self.selenium, By.XPATH, "//*[@id='page-index' and @data-page='1']")

        # Expected result for previous button
        data_page1 = index_page.get_attribute("data-page")
        expected1 = "1"

        # Check result for previous 
        self.assertEqual(data_page1, expected1)

    def test_index_page_2_posts_should_load(self):
        self.selenium.get('http://127.0.0.1:8000/')
        next_page = self.wait_for_element(self.selenium, By.XPATH, '//*[@id="next"]')

        # Action
        next_page.click()
        self.wait_for_element(self.selenium, By.CLASS_NAME, 'card-text')

        # Extract elements from page
        cards = self.selenium.find_elements_by_class_name('card-body')
        card_titles = self.selenium.find_elements_by_class_name('card-title')
        card_subtitles = self.selenium.find_elements_by_class_name('card-subtitle')
        card_texts = self.selenium.find_elements_by_class_name('card-text')

        # Expected result
        expected = 2

        # Check results
        self.assertEqual(len(cards), expected)
        self.assertEqual(len(card_titles), expected)
        self.assertEqual(len(card_subtitles), expected)
        self.assertEqual(len(card_texts), expected)

    def test_index_page_1_profile_should_load(self):
        self.selenium.get('http://127.0.0.1:8000/')
        self.wait_for_element(self.selenium, By.CLASS_NAME, 'card-text')

        # Extract elements from page
        profile_link = self.selenium.find_element(by=By.XPATH, value='//*[@id="posts-list"]/div[1]//a')
        
        # Action
        profile_link.click()
        
        # Check result
        self.assertEqual(self.selenium.title, "Profile")

    def tearDown(self):
        self.selenium.quit()

    if __name__ == "__main__":
        chrome_options = Options()
        webdriver_service = Service("/home/deborahly/chromedriver/stable/chromedriver")
        selenium = webdriver.Chrome(service=webdriver_service, options=chrome_options)
        selenium.get('http://127.0.0.1:8000/')

        # Test
        title = selenium.title