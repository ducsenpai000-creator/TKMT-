from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
import pandas as pd
import time

# ===== Nhập email/password =====
email_input = input("Nhập email: ")
password_input = getpass("Nhập mật khẩu: ")

# ===== Cấu hình Firefox =====
gecko_path = r"C:/GIT/selenium/geckodriver.exe"
service = Service(gecko_path)
options = webdriver.FirefoxOptions()
options.binary_location = r"C:/Program Files/Mozilla Firefox/firefox.exe"  
options.headless = False

driver = webdriver.Firefox(service=service, options=options)

# ===== Truy cập VnExpress =====
driver.get("https://vnexpress.net/")
time.sleep(3)

# ===== Login (giữ nguyên) =====
try:
    email_box = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "myvne_email_input"))
    )
    email_box.send_keys(email_input)

    login_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='checkAccount']"))
    )
    login_button.click()

    password_box = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "myvne_password_input"))
    )
    password_box.send_keys(password_input)

    login_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='myvne_button_login']"))
    )
    login_button.click()
except:
    print("Không tìm thấy form login, tiếp tục cào dữ liệu...")

time.sleep(3)

# ===== Lấy 3 bài đầu =====
articles = driver.find_elements(By.TAG_NAME, "article")
data = []

for art in articles[:10]:
    try:
        link_elem = art.find_element(By.TAG_NAME, "a")
        link = link_elem.get_attribute("href")
    except:
        continue

    try:
        title = art.find_element(By.TAG_NAME, "h3").text
        if not title:
            title = art.find_element(By.TAG_NAME, "h2").text
    except:
        title = ""

    try:
        author = art.find_element(By.CSS_SELECTOR, ".author_mail").text
    except:
        author = "Không đề cập"

    data.append({
        "title": title,
        "author": author,
        "link": link
    })

# ===== Xuất Excel =====
df = pd.DataFrame(data)
df.to_excel("vnexpress_top10.xlsx", index=False)
driver.quit()
print("Dữ liệu đã được lưu vào vnexpress_top3.xlsx")