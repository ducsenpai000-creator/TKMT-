from selenium import webdriver
from selenium.webdriver.common.by import By
import time 

driver = webdriver.Chrome()
driver.get("https://cpstest.org/")
time.sleep(2)

try:
    while True:
        driver.find_element(By.ID, "clickarea").click()
        time.sleep(0.00000000000000000000000001)
except:
    driver.quit()
