from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
import time

email = input("Nhập email / MSSV: ")
password_text = getpass("Nhập mật khẩu: ")

gecko_path = r"C:/GIT/project 02/geckodriver.exe"
service = Service(gecko_path)

options = webdriver.firefox.options.Options()
options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
options.headless = False

driver = webdriver.Firefox(options=options, service=service)

url = "https://sso.hutech.edu.vn/login-sso?client_id=7c2075d1-9539-4061-b32b-ca9873f13e13&backlink=https:%2F%2Fhocvudientu.hutech.edu.vn&redirect=%2Fdang-nhap%3FReturnUrl%3D%2F"
driver.get(url)

username = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
)
username.send_keys(email)

password = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
)
password.send_keys(password_text)

time.sleep(1)

login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-primary.waves-effect.waves-themed.w-100"))
)
login_button.click()

print("Đã gửi yêu cầu đăng nhập!")

time.sleep(20)

driver.quit()
