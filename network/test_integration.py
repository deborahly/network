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

def wait_for_element(webdriver, method, query, wait_time=3):
        return WebDriverWait(webdriver, wait_time).until(EC.presence_of_element_located((method, query)))

def wait_until_not_present(webdriver, method, query, wait_time=3):
    return WebDriverWait(webdriver, wait_time).until_not(EC.presence_of_element_located((method, query)))

# Create your tests here.
class IntegrationTestCase(StaticLiveServerTestCase):
    
    USERNAME1 = "deborahly"
    USER1_PASSWORD = "12345"
    USERNAME2 = "anderson"
    USER2_PASSWORD = "12345"
    POSTS_PER_PAGE = 10
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

        # Create 20 posts
        Post.objects.create(poster=user1, content="I saw a dog")
        Post.objects.create(poster=user2, content="I saw a cat")
        Post.objects.create(poster=user1, content="I saw a racoon")
        Post.objects.create(poster=user2, content="I saw a skunk")
        Post.objects.create(poster=user1, content="I saw a squirrel")
        Post.objects.create(poster=user2, content="I saw a cardinal")
        Post.objects.create(poster=user1, content="I saw a marmot")
        Post.objects.create(poster=user2, content="I saw a badger")
        Post.objects.create(poster=user1, content="I saw a kookaburra")
        Post.objects.create(poster=user2, content="I saw a woodpecker")
        Post.objects.create(poster=user1, content="I saw a butterfly")
        Post.objects.create(poster=user2, content="I saw a spider")
        Post.objects.create(poster=user1, content="I saw a monkey")
        Post.objects.create(poster=user2, content="I saw a ladybug")
        Post.objects.create(poster=user1, content="I saw a snake")
        Post.objects.create(poster=user2, content="I saw a cow")
        Post.objects.create(poster=user1, content="I saw a horse")
        Post.objects.create(poster=user2, content="I saw a gecko")
        Post.objects.create(poster=user1, content="I saw a lhama")
        Post.objects.create(poster=user2, content="I saw a bat")
        Post.objects.create(poster=user1, content="I saw an alpaca")
        Post.objects.create(poster=user2, content="I saw a beetle")
        
        self.selenium = self.create_driver()

    def test_index_page_1_should_exist(self):
        self.selenium.get(self.live_server_url)

        self.assertEqual(self.selenium.title, "Index")

    def test_index_page_1_posts_should_load(self):
        self.selenium.get(self.live_server_url)

        wait_for_element(self.selenium, By.XPATH, f'//*[@id="posts-list"]/div[{self.POSTS_PER_PAGE}]//p[contains(@class, "card-text")]')

        cards = self.selenium.find_elements_by_class_name("card-body")
        card_titles = self.selenium.find_elements_by_class_name("card-title")
        card_dates = self.selenium.find_elements_by_class_name("date")
        card_texts = self.selenium.find_elements_by_class_name("card-text")

        expected = self.POSTS_PER_PAGE

        self.assertEqual(len(cards), expected)
        self.assertEqual(len(card_titles), expected)
        self.assertEqual(len(card_dates), expected)
        self.assertEqual(len(card_texts), expected)

    def test_index_page_1_likes_should_appear(self):
        self.selenium.get(self.live_server_url)
        
        wait_for_element(self.selenium, By.XPATH, '//*[@id="posts-list"]/div[1]//span[.="0"]')

    def test_index_page_1_previous_button_should_be_disabled(self):
        self.selenium.get(self.live_server_url)
        
        previous_page = wait_for_element(self.selenium, By.ID, "previous")
        disabled = previous_page.get_attribute("disabled")

        self.assertEqual(disabled, "true")
    
    def test_index_page_1_next_previous_buttons_should_work(self):
        self.selenium.get(self.live_server_url)
        
        next_page = wait_for_element(self.selenium, By.ID, "next")
        next_page.click()

        wait_for_element(self.selenium, By.XPATH, "//*[@id='page-index' and @data-page='2']")
        wait_for_element(self.selenium, By.XPATH, f'//*[@id="posts-list"]/div[{self.POSTS_PER_PAGE}]//p[contains(@class, "card-text")]')

        cards = self.selenium.find_elements_by_class_name('card-body')
        card_titles = self.selenium.find_elements_by_class_name('card-title')
        card_subtitles = self.selenium.find_elements_by_class_name('date')
        card_texts = self.selenium.find_elements_by_class_name('card-text')

        expected = self.POSTS_PER_PAGE

        self.assertEqual(len(cards), expected)
        self.assertEqual(len(card_titles), expected)
        self.assertEqual(len(card_subtitles), expected)
        self.assertEqual(len(card_texts), expected)

        previous_page = wait_for_element(self.selenium, By.ID, "previous")
        previous_page.click()

        wait_for_element(self.selenium, By.XPATH, "//*[@id='page-index' and @data-page='1']")

    def test_index_page_1_profile_should_load(self):
        self.selenium.get(self.live_server_url)

        profile_link = wait_for_element(self.selenium, By.XPATH, '//*[@id="posts-list"]/div[1]//a[contains(@href, "profile")]')
        profile_link.click()
        time.sleep(2)
        
        self.assertEqual(self.selenium.title, "Profile") 

    def test_authenticated_index_page_1_should_exist(self):
        self.login(self.selenium)

        self.assertEqual(self.selenium.title, "Index")

    def test_authenticated_index_page_1_posts_should_load(self):
        self.login(self.selenium)
        
        wait_for_element(self.selenium, By.XPATH, f'//*[@id="posts-list"]/div[{self.POSTS_PER_PAGE}]//p[contains(@class, "card-text")]')

        cards = self.selenium.find_elements_by_class_name("card-body")
        card_titles = self.selenium.find_elements_by_class_name("card-title")
        card_dates = self.selenium.find_elements_by_class_name("date")
        card_texts = self.selenium.find_elements_by_class_name("card-text")

        expected = self.POSTS_PER_PAGE

        self.assertEqual(len(cards), expected)
        self.assertEqual(len(card_titles), expected)
        self.assertEqual(len(card_dates), expected)
        self.assertEqual(len(card_texts), expected)

    def test_authenticated_index_page_1_give_like_should_work(self):
        self.login(self.selenium)

        wait_for_element(self.selenium, By.XPATH, '//*[@id="posts-list"]/div[1]//span[.="0"]')
        
        like_link = wait_for_element(self.selenium, By.XPATH, '//*[@id="posts-list"]/div[1]//a[contains(text(), "Like")]')
        like_link.click()

        wait_for_element(self.selenium, By.XPATH, '//*[@id="posts-list"]/div[1]//span[.="1"]')

        unlike_link = wait_for_element(self.selenium, By.XPATH, '//*[@id="posts-list"]/div[1]//a[contains(text(), "Unlike")]')
        unlike_link.click()

        wait_for_element(self.selenium, By.XPATH, '//*[@id="posts-list"]/div[1]//span[.="0"]')

    def test_authenticated_index_page_1_previous_button_should_be_disabled(self):
        self.login(self.selenium)

        previous_page = wait_for_element(self.selenium, By.ID, "previous")
        disabled = previous_page.get_attribute("disabled")
    
        self.assertEqual(disabled, "true")
    
    def test_authenticated_index_page_1_next_previous_buttons_should_work(self):
        self.login(self.selenium)

        next_page = wait_for_element(self.selenium, By.ID, "next")
        next_page.click()

        wait_for_element(self.selenium, By.XPATH, "//*[@id='page-index' and @data-page='2']")
        wait_for_element(self.selenium, By.XPATH, f'//*[@id="posts-list"]/div[{self.POSTS_PER_PAGE}]//p[contains(@class, "card-text")]')

        cards = self.selenium.find_elements_by_class_name('card-body')
        card_titles = self.selenium.find_elements_by_class_name('card-title')
        card_subtitles = self.selenium.find_elements_by_class_name('date')
        card_texts = self.selenium.find_elements_by_class_name('card-text')

        expected = self.POSTS_PER_PAGE

        self.assertEqual(len(cards), expected)
        self.assertEqual(len(card_titles), expected)
        self.assertEqual(len(card_subtitles), expected)
        self.assertEqual(len(card_texts), expected)

        previous_page = wait_for_element(self.selenium, By.ID, "previous")
        previous_page.click()

        wait_for_element(self.selenium, By.XPATH, "//*[@id='page-index' and @data-page='1']")

    def test_authenticated_index_page_1_profile_should_load(self):
        self.login(self.selenium)

        profile_link = wait_for_element(self.selenium, By.XPATH, '//*[@id="posts-list"]/div[1]//a[contains(@href, "profile")]')
        profile_link.click()
        time.sleep(2)
        
        self.assertEqual(self.selenium.title, "Profile") 

    def test_authenticated_index_page_1_post_can_be_created_and_deleted(self):
        self.login(self.selenium)

        post_content = wait_for_element(self.selenium, By.ID, "new-post-content")
        post_button = wait_for_element(self.selenium, By.ID, "new-post-button")
        post_content.send_keys("I saw two cats")
        post_button.click()

        wait_for_element(self.selenium, By.XPATH, "//*[.='I saw two cats']")

        delete_button = wait_for_element(self.selenium, By.XPATH, '//*[.="I saw two cats"]/../a[contains(text(), "Delete")]')
        delete_button.click()

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