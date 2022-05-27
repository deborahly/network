from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path

service_object = Service(binary_path)
driver = webdriver.Chrome(service=service_object)

