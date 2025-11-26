from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://gomotungkinh.com/")
time.sleep(5)
try :
    while True :
        popup_close_button = driver.find_element(By.ID, "bonk").click()
        time.sleep(2)
except:
    driver.quit()