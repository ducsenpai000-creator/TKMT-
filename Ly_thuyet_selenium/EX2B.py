from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd

gecko_path = r"C:/GIT/project 02/geckodriver.exe"
service = Service(gecko_path)
options = Options()
options.headless = False  

driver = webdriver.Firefox(service=service, options=options)

url = "https://gochek.vn/collections/all"
driver.get(url)
time.sleep(3)

SCROLL_PAUSE_TIME = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

time.sleep(1)

cards = driver.find_elements(By.XPATH,
    "//div[.//img and (.//h3 or .//h2) and .//*[contains(text(),'₫')]]"
)

print(f"{len(cards)}")

data = []
for card in cards:
    try:
        # Tên sản phẩm
        name = ""
        try:
            name = card.find_element(By.TAG_NAME, "h3").text.strip()
        except:
            name = card.find_element(By.TAG_NAME, "h2").text.strip()
    except:
        continue
    
    # Ảnh sản phẩm
    img = ""
    try:
        img = card.find_element(By.TAG_NAME, "img").get_attribute("src")
    except:
        img = ""
    
    # Giá sản phẩm
    price = ""
    try:
        texts = card.text.split()
        for t in texts:
            if "₫" in t:
                price = t
                break
    except:
        price = ""
    
    if name:
        data.append({
            "Tên sản phẩm": name,
            "Giá bán": price,
            "Hình ảnh": img
        })

# Loại bỏ trùng theo tên sản phẩm 
df = pd.DataFrame(data)
df_unique = df.drop_duplicates(subset=['Tên sản phẩm']).reset_index(drop=True)

df_unique.to_excel("gochek_all_products_unique.xlsx", index=False)
driver.quit()
