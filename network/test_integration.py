"""
# Filename: run_self.selenium.py
"""

## Run selenium and chrome driver to scrape data from cloudbytes.dev
from cgi import test
import profile
import time
from typing import Text
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .models import User, Post, Follow, Like
import django.core.management.commands.runserver as runserver

def wait_for_element(webdriver, method, query, wait_time=2):
        return WebDriverWait(webdriver, wait_time).until(EC.presence_of_element_located((method, query)))

def wait_until_not_present(webdriver, method, query, wait_time=2):
    return WebDriverWait(webdriver, wait_time).until_not(EC.presence_of_element_located((method, query)))

# Create your tests here.
class IntegrationTestCase(StaticLiveServerTestCase):
    
    USERNAME1 = "deborahly"
    USER1_PASSWORD = "12345"
    USERNAME2 = "anderson"
    USER2_PASSWORD = "12345"
    host = "127.0.0.1"
    port = 8000

    def create_driver(self):
        # Setup chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless") # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")

        # Set path to chromedriver as per your configuration
        webdriver_service = Service("/opt/chromedriver")

        # Choose Chrome Browser
        return webdriver.Chrome(service=webdriver_service, options=chrome_options)

    def login(self, webdriver):
        webdriver.get(self.live_server_url)
        login_link = wait_for_element(webdriver, By.XPATH, '//a[@href="/login"]')
        login_link.click()

        username = wait_for_element(webdriver, By.XPATH, '//*[@name="username"]')
        username.send_keys(self.USERNAME1)
        password = wait_for_element(webdriver, By.XPATH, '//*[@name="password"]')
        password.send_keys(self.USER1_PASSWORD)

        login_button = wait_for_element(webdriver, By.XPATH, '//input[@value="Login"]')
        login_button.click()

    def setUp(self):
        super().setUp()

        user1 = User.objects.create_user(username=self.USERNAME1, email=f"{self.USERNAME1}@example.com", password=self.USER1_PASSWORD)
        user2 = User.objects.create_user(username=self.USERNAME2, email=f"{self.USERNAME2}y@example.com", password=self.USER2_PASSWORD)

        user1.is_superuser = True
        user1.is_staff = True
        user1.save()

        Post.objects.create(poster=user1, content="I saw a dog")
        Post.objects.create(poster=user2, content="I saw a cat")
        Post.objects.create(poster=user1, content="I saw a racoon")
        Post.objects.create(poster=user2, content="I saw a skunk")

        self.selenium = self.create_driver()

    def test_index_page_should_exist(self):
        self.selenium.get(self.live_server_url)
        
        # Check result
        self.assertEqual(self.selenium.title, "Index")

    def test_index_page_1_posts_should_load(self):
        self.selenium.get(self.live_server_url)
        
        wait_for_element(self.selenium, By.CLASS_NAME, "card-text")

        # Extract elements from page
        cards = self.selenium.find_elements_by_class_name("card-body")
        card_titles = self.selenium.find_elements_by_class_name("card-title")
        card_subtitles = self.selenium.find_elements_by_class_name("date")
        card_texts = self.selenium.find_elements_by_class_name("card-text")

        # Expected result
        expected = 2

        # Check results
        self.assertEqual(len(cards), expected)
        self.assertEqual(len(card_titles), expected)
        self.assertEqual(len(card_subtitles), expected)
        self.assertEqual(len(card_texts), expected)

    def test_index_page_1_likes_should_appear(self):
        self.selenium.get(self.live_server_url)
        wait_for_element(self.selenium, By.XPATH, '//*[@id="posts-list"]/div[2]/div/span/span')
        
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
        self.selenium.get(self.live_server_url)
        wait_for_element(self.selenium, By.XPATH, '//*[@id="previous"]')

        # Extract elements from page
        previous_page = self.selenium.find_element(by=By.XPATH, value='//*[@id="previous"]')
        disabled = previous_page.get_attribute("disabled")

        # Expected result
        expected = "true"

        # Check result
        self.assertEqual(disabled, expected)
    
    def test_index_page_1_next_previous_buttons_should_work(self):
        self.selenium.get(self.live_server_url)
        wait_for_element(self.selenium, By.XPATH, '//*[@id="next"]')

        # Extract next page button from page 1
        next_page = self.selenium.find_element(by=By.XPATH, value='//*[@id="next"]')
        
        # Action
        next_page.click()
        index_page = wait_for_element(self.selenium, By.XPATH, "//*[@id='page-index' and @data-page='2']")

        # Expected result for next button
        data_page2 = index_page.get_attribute("data-page")
        expected = "2"

        # Check result for next button
        self.assertEqual(data_page2, expected)

        # Extract cards from page 2
        cards = self.selenium.find_elements_by_class_name('card-body')
        card_titles = self.selenium.find_elements_by_class_name('card-title')
        card_subtitles = self.selenium.find_elements_by_class_name('date')
        card_texts = self.selenium.find_elements_by_class_name('card-text')

        # Expected result for posts on page 2
        expected = 2

        # Check results
        self.assertEqual(len(cards), expected)
        self.assertEqual(len(card_titles), expected)
        self.assertEqual(len(card_subtitles), expected)
        self.assertEqual(len(card_texts), expected)

        # Extract previous buttons from page 2
        previous_page = self.selenium.find_element(by=By.XPATH, value='//*[@id="previous"]')
        
        # Action
        previous_page.click()
        index_page = wait_for_element(self.selenium, By.XPATH, "//*[@id='page-index' and @data-page='1']")

        # Expected result for previous button
        data_page1 = index_page.get_attribute("data-page")
        expected = "1"

        # Check result for previous 
        self.assertEqual(data_page1, expected)

    def test_index_page_1_profile_should_load(self):
        self.selenium.get(self.live_server_url)
        wait_for_element(self.selenium, By.CLASS_NAME, 'card-text')

        # Extract elements from page
        profile_link = self.selenium.find_element(by=By.XPATH, value='//*[@id="posts-list"]/div[1]//a')
        
        # Action
        profile_link.click()
        
        # Check result
        self.assertEqual(self.selenium.title, "Profile") 

    def test_authenticated_index_page_should_exist(self):
        self.login(self.selenium)
        
        # Check result
        self.assertEqual(self.selenium.title, "Index")

    def test_authenticated_index_page_1_posts_should_load(self):
        self.login(self.selenium)
        
        wait_for_element(self.selenium, By.CLASS_NAME, "card-text")

        # Extract elements from page
        cards = self.selenium.find_elements_by_class_name("card-body")
        card_titles = self.selenium.find_elements_by_class_name("card-title")
        card_subtitles = self.selenium.find_elements_by_class_name("date")
        card_texts = self.selenium.find_elements_by_class_name("card-text")

        # Expected result
        expected = 2

        # Check results
        self.assertEqual(len(cards), expected)
        self.assertEqual(len(card_titles), expected)
        self.assertEqual(len(card_subtitles), expected)
        self.assertEqual(len(card_texts), expected)

    def test_authenticated_index_page_1_give_like_should_work(self):
        self.login(self.selenium)

        # Test likes number
        wait_for_element(self.selenium, By.XPATH, '//*[@id="posts-list"]/div[1]/div/span/span[.="0"]')
        
        # Test like post
        like_link = wait_for_element(self.selenium, By.XPATH, '//*[@id="posts-list"]/div[1]//a[contains(text(), "Like")]')
        like_link.click()
        wait_for_element(self.selenium, By.XPATH, '//*[@id="posts-list"]/div[1]/div/span/span[.="1"]')

        # Test unlike post
        unlike_link = wait_for_element(self.selenium, By.XPATH, '//*[@id="posts-list"]/div[1]//a[contains(text(), "Unlike")]')
        unlike_link.click()
        wait_for_element(self.selenium, By.XPATH, '//*[@id="posts-list"]/div[1]/div/span/span[.="0"]')

    def test_authenticated_index_page_1_previous_button_should_be_disabled(self):
        self.login(self.selenium)

        wait_for_element(self.selenium, By.XPATH, '//*[@id="previous"]')

        # Extract elements from page
        previous_page = self.selenium.find_element(by=By.XPATH, value='//*[@id="previous"]')
        disabled = previous_page.get_attribute("disabled")

        # Expected result
        expected = "true"

        # Check result
        self.assertEqual(disabled, expected)
    
    def test_authenticated_index_page_1_next_previous_buttons_should_work(self):
        self.login(self.selenium)

        wait_for_element(self.selenium, By.XPATH, '//*[@id="next"]')

        # Extract next button from page 1
        next_page = self.selenium.find_element(by=By.XPATH, value='//*[@id="next"]')
        
        # Action
        next_page.click()
        index_page = wait_for_element(self.selenium, By.XPATH, "//*[@id='page-index' and @data-page='2']")

        # Expected result for next button
        data_page2 = index_page.get_attribute("data-page")
        expected = "2"

        # Check result for next button
        self.assertEqual(data_page2, expected)

        # Extract cards from page 2
        cards = self.selenium.find_elements_by_class_name('card-body')
        card_titles = self.selenium.find_elements_by_class_name('card-title')
        card_subtitles = self.selenium.find_elements_by_class_name('date')
        card_texts = self.selenium.find_elements_by_class_name('card-text')

        # Expected result
        expected = 2

        # Check results
        self.assertEqual(len(cards), expected)
        self.assertEqual(len(card_titles), expected)
        self.assertEqual(len(card_subtitles), expected)
        self.assertEqual(len(card_texts), expected)
        
        # Extract previous button from page 2
        previous_page = self.selenium.find_element(by=By.XPATH, value='//*[@id="previous"]')

        # Action
        previous_page.click()
        index_page = wait_for_element(self.selenium, By.XPATH, "//*[@id='page-index' and @data-page='1']")

        # Expected result for previous button
        data_page1 = index_page.get_attribute("data-page")
        expected = "1"

        # Check result for previous 
        self.assertEqual(data_page1, expected)

    def test_authenticated_index_page_1_profile_should_load(self):
        self.login(self.selenium)

        wait_for_element(self.selenium, By.CLASS_NAME, 'card-text')

        # Extract elements from page
        profile_link = self.selenium.find_element(by=By.XPATH, value='//*[@id="posts-list"]/div[1]//a')
        
        # Action
        profile_link.click()
        
        # Check result
        self.assertEqual(self.selenium.title, "Profile")

    def test_authenticated_index_page_1_post_can_be_created_and_deleted(self):
        self.login(self.selenium)

        # Extract field and button from page
        content_field = wait_for_element(self.selenium, By.ID, "new-post-content")
        post_button = wait_for_element(self.selenium, By.ID, "new-post-button")
        
        # Action
        content_field.send_keys("I saw two cats")
        post_button.click()

        # Check result
        wait_for_element(self.selenium, By.XPATH, "//*[.='I saw two cats']")

        # Extract post content and delete button from page
        delete_button = wait_for_element(self.selenium, By.XPATH, '//*[.="I saw two cats"]/../a[contains(text(), "Delete")]')

        # Action
        delete_button.click()

        # Check result
        wait_until_not_present(self.selenium, By.XPATH, "//*[.='I saw two cats']")

    def tearDown(self):
        self.selenium.quit()
        super().tearDown()

    # if __name__ == "__main__":
    #     chrome_options = Options()
    #     webdriver_service = Service("/home/deborahly/chromedriver/stable/chromedriver")
    #     selenium = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    #     selenium.get('http://127.0.0.1:8000/')

    #     # Test
    #     title = selenium.title