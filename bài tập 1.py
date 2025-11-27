from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Khởi tạo WebDriver
driver = webdriver.Chrome()

# Mở full màn hình 
driver.maximize_window()

# Mở trang Wikipedia
url = "https://en.wikipedia.org/wiki/List_of_painters_by_name"
driver.get(url)

# Đợi 2 giây cho trang load
time.sleep(2)

# Lấy tất cả thẻ <a>
tags = driver.find_elements(By.TAG_NAME, "a")

# Lấy danh sách các link
links = [tag.get_attribute("href") for tag in tags]

# Xuất thông tin
for link in links:
    print(link)

# Đóng WebDriver
driver.quit()
