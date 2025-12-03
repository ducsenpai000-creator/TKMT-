from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time

# Đường dẫn đến file thực thi geckodriver
gecko_path = r"C:/GIT/project 02/geckodriver.exe"

# Khởi tạo đối tượng dịch vụ với đường dẫn geckodriver
ser = Service(gecko_path)

# Tạo tuỳ chọn
options = webdriver.firefox.options.Options()
options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
# Thiết lập firefox chỉ hiển thị giao diện
options.headless = False

# Khởi tạo driver
driver = webdriver.Firefox(options=options, service=ser)

# Tạo url
url = "http://pythonscraping.com/pages/javascript/ajaxDemo.html"

# Truy cập
driver.get(url)

# In ra nội dung của trang web
print("Before: ----------------------------------------\n")
print(driver.page_source)

# Tạm dừng khoảng 3 giây
time.sleep(10)

# In lại
print("\n\n\nAfter: ----------------------------------------\n")
print(driver.page_source)

# Đóng browser
driver.quit()
