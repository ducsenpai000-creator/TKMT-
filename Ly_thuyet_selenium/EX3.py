from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
import time
import pandas as pd

# Đường dẫn đến file thực thi geckodriver
gecko_path = r"C:/GIT/project 02/geckodriver.exe"

# Khởi tởi đối tượng dịch vụ với đường geckodriver
ser = Service(gecko_path)

# Tạo tùy chọn
options = webdriver.firefox.options.Options()
options.binary_location ="C:/Program Files/Mozilla Firefox/firefox.exe"
# Thiết lập firefox chỉ hiện thị giao diện
options.headless = False

# Khởi tạo driver
driver = webdriver.Firefox(options = options, service=ser)

# Tạo url
url = 'http://pythonscraping.com/pages/files/form.html'

# Truy cập
driver.get(url)

# Tạm dừng khoảng 2 giây
time.sleep(2)

firstname_input = driver.find_element(By.XPATH, "//input[@name='firstname']")
lastname_input = driver.find_element(By.XPATH, "//input[@name='lastname']")

firstname_input.send_keys('Minh Duc')
time.sleep(1)
lastname_input.send_keys("Tran")

time.sleep(2)
buttton = driver.find_element(By.XPATH, "//input[@type='submit']")
buttton.click()
time.sleep(5)

driver.quit()