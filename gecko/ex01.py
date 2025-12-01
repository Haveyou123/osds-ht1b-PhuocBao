from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import time


gecko_path = r"C:/KPDL/gecko/geckodriver.exe"
service = Service(gecko_path)

options = webdriver.FirefoxOptions()
options.binary_location = r"C:/Program Files/Mozilla Firefox/firefox.exe"
options.headless = False

driver = webdriver.Firefox(service=service, options=options)

url = 'http://pythonscraping.com/pages/javascript/ajaxDemo.html'
driver.get(url)

print("Before : ===========================\n")
print(driver.page_source)

time.sleep(3)

print("\n\nAfter : ===========================\n")
print(driver.page_source)

driver.quit()
