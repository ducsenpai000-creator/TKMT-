from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import pandas as pd
import sqlite3

# CẤU HÌNH SELENIUM
gecko_path = r"C:/GIT/selenium/Ly_thuyet_selenium/geckodriver.exe"
options = webdriver.firefox.options.Options()
options.binary_location = r"C:/Program Files/Mozilla Firefox/firefox.exe"
options.headless = False

driver = webdriver.Firefox(service=Service(gecko_path), options=options)
driver.get("https://nhathuoclongchau.com.vn/thuc-pham-chuc-nang/vitamin-khoang-chat")

time.sleep(2)

# CUỘN TRANG + CLICK XEM THÊM
for _ in range(10):
    try:
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for btn in buttons:
            if "Xem thêm" in btn.text:
                btn.click()
                time.sleep(1)
                break
    except:
        pass

for _ in range(60):
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ARROW_DOWN)
    time.sleep(0.02)

time.sleep(2)

# TẠO DATABASE + TABLE SQLite
db = "longchau_db.sqlite"
conn = sqlite3.connect(db)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sanpham (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_url TEXT UNIQUE,
    product_name TEXT,
    price TEXT,
    original_price TEXT,
    unit TEXT
)
""")
conn.commit()

# TÌM TẤT CẢ SP
buttons = driver.find_elements(By.XPATH, "//button[text()='Chọn mua']")
print("Tổng sản phẩm tìm được:", len(buttons))

# CÀO TỪNG SP + LƯU VÀO SQLite
for index, bt in enumerate(buttons, 1):

    div = bt
    for _ in range(3):
        div = div.find_element(By.XPATH, "./..")

    try:
        name = div.find_element(By.TAG_NAME, 'h3').text
    except:
        name = ""

    try:
        price = div.find_element(By.CLASS_NAME, 'text-blue-5').text
    except:
        price = ""

    # Tìm giá gốc 
    try:
        original_price = div.find_element(By.CLASS_NAME, "line-through").text
    except:
        original_price = price  # nếu không có giá gốc thì để bằng giá bán

    try:
        link = div.find_element(By.TAG_NAME, 'a').get_attribute('href')
    except:
        continue


        # Lấy unit (đơn vị)
    try:
        # Mở tab mới
        driver.execute_script("window.open(arguments[0]);", link)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)

        # Tìm đúng phần "Quy cách" của sản phẩm
        try:
            unit = driver.find_element(
                By.XPATH,
                "//div[contains(@class,'label') and contains(text(),'Quy cách')]/following-sibling::div[1]"
            ).text
        except:
            # Nếu không có block Quy cách chuẩn → fallback tìm chữ Hộp/Chai/Tuýp/Vỉ
            try:
                unit = driver.find_element(
                    By.XPATH,
                    "//*[contains(text(),'Hộp') or contains(text(),'Chai') or contains(text(),'Tuýp') or contains(text(),'Vỉ')]"
                ).text
            except:
                unit = "Không rõ"

        # Đóng tab và quay về tab chính
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    except:
        unit = "Không rõ"


    # LƯU VÀO SQLite
    try:
        cursor.execute("""
        INSERT OR IGNORE INTO sanpham(product_url, product_name, price, original_price, unit)
        VALUES (?,?,?,?,?)
        """, (link, name, price, original_price, unit))

        conn.commit()

    except Exception as e:
        print("Error:", e)

driver.quit()
conn.close()