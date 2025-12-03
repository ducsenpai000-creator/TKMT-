from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re

# ============================
# DataFrame
# ============================
columns = [
    "Tên trường", 
    "Tên viết tắt",
    "Loại trường",        # Công lập / Tư thục / ...
    "Năm thành lập",
    "Hiệu trưởng",
    "Mã trường",
    "Website",
    "Địa chỉ"
]

df = pd.DataFrame(columns=columns)

# ============================
# Chrome
# ============================
driver = webdriver.Chrome()
url = "https://vi.wikipedia.org/wiki/Danh_s%C3%A1ch_tr%C6%B0%E1%BB%9Dng_%C4%91%E1%BA%A1i_h%E1%BB%8Dc,_h%E1%BB%8Dc_vi%E1%BB%87n_v%C3%A0_cao_%C4%91%E1%BA%B3ng_t%E1%BA%A1i_Vi%E1%BB%87t_Nam"
driver.get(url)
time.sleep(3)

# ============================
# Lấy link các trường
# ============================
a_tags = driver.find_elements(By.TAG_NAME, "a")
school_links = []

for a in a_tags:
    try:
        href = a.get_attribute("href")
        text = a.text.strip()
        if href and "/wiki/" in href and text and "Đại học" in text:
            school_links.append(href)
    except:
        continue

school_links = list(dict.fromkeys(school_links))
print("Tìm thấy", len(school_links), "link trường.")

# ============================
# Safe Text
# ============================
def safe_text(by, value):
    try:
        return driver.find_element(by, value).text.strip()
    except:
        return ""

# ============================
# Lấy từ infobox
# ============================
def get_info(alias_list):
    for alias in alias_list:
        try:
            return driver.find_element(
                By.XPATH, f"//th[contains(text(), '{alias}')]/following-sibling::td"
            ).text.strip()
        except:
            continue
    return ""

# ============================
# Xác định loại trường (Công lập / Tư thục)
# ============================
def detect_school_type(page_text):
    text = page_text.lower()

    pub_kw = ["công lập", "public", "nhà nước", "quốc gia", "trọng điểm"]
    pri_kw = ["tư thục", "private", "ngoài công lập", "tư lập", "dân lập"]

    for k in pub_kw:
        if k in text:
            return "Công lập"

    for k in pri_kw:
        if k in text:
            return "Tư thục"

    return "Không rõ"

# ============================
# Bắt đầu crawl
# ============================
for idx, link in enumerate(school_links):
    print(f"{idx+1}/{len(school_links)} → {link}")
    driver.get(link)
    time.sleep(1.3)

    name = safe_text(By.TAG_NAME, "h1")

    short_name = get_info(["Tên viết tắt", "Viết tắt"])

    # Lấy mô tả đầu trang để xác định loại trường
    try:
        intro_text = driver.find_element(By.XPATH, "//p[1]").text
    except:
        intro_text = ""

    # Lấy full text trang để tăng độ chính xác
    try:
        full_text = driver.find_element(By.TAG_NAME, "body").text
    except:
        full_text = intro_text

    school_type = detect_school_type(full_text)

    # Năm thành lập
    established = get_info(["Năm thành lập", "Thành lập"])
    year_match = re.search(r"(18|19|20)\d{2}", established)
    established = year_match.group(0) if year_match else established

    president = get_info(["Hiệu trưởng", "Giám đốc"])
    code = get_info(["Mã trường", "Mã tuyển sinh"])
    website = get_info(["Website"])

    address = get_info(["Địa chỉ", "Trụ sở", "Cơ sở", "Đặt tại"])

    df.loc[len(df)] = [
        name, short_name, school_type,
        established, president, code,
        website, address
    ]

driver.quit()

df.to_excel("vietnam_universities_clean.xlsx", index=False)
