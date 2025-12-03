from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re
import sqlite3

painters_df = pd.DataFrame(columns=['name', 'birth', 'death', 'nationality'])

driver = webdriver.Chrome()
url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22F%22"
driver.get(url)
time.sleep(3)

ul_tags = driver.find_elements(By.TAG_NAME, "ul")
ul_painters = None
for ul in ul_tags:
    if "Fragonard" in ul.text:
        ul_painters = ul
        break

if ul_painters is None:
    print("Could not find the painters list.")
    driver.quit()
    exit()

li_tags = ul_painters.find_elements(By.TAG_NAME, "li")
all_links = []
for li in li_tags:
    try:
        all_links.append(li.find_element(By.TAG_NAME, "a").get_attribute("href"))
    except:
        continue

for count, link in enumerate(all_links):
    if count >= 5:
        break

    driver.get(link)
    time.sleep(2)

    # NAME
    try:
        name = driver.find_element(By.TAG_NAME, "h1").text
    except:
        name = ""

    # BIRTH
    try:
        birth_text = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td").text
        birth_match = re.findall(r'\d{1,2}\s[A-Za-z]+\s\d{4}|\d{4}', birth_text)
        birth = birth_match[0] if birth_match else ""
    except:
        birth = ""

    # DEATH
    try:
        death_text = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td").text
        death_match = re.findall(r'\d{1,2}\s[A-Za-z]+\s\d{4}|\d{4}', death_text)
        death = death_match[0] if death_match else ""
    except:
        death = ""

    # NATIONALITY
    # NATIONALITY từ Birth place
    try:
        birth_td = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
        birth_text = birth_td.text.strip()
        # thường birth_text: "15 April 1732 Grasse, France"
        if ',' in birth_text:
            citizen = birth_text.split(',')[-1].strip()
        else:
            parts = birth_text.split()
            citizen = parts[-1] if parts else "Unknown"
    except:
        citizen = "Unknown"




    painters_df.loc[len(painters_df)] = [name, birth, death, citizen]

driver.quit()

conn = sqlite3.connect("painters.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS painters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    birth TEXT,
    death TEXT,
    nationality TEXT
)
""")

# Chèn dữ liệu
sql_insert = """
INSERT INTO painters (name, birth, death, nationality)
VALUES (?, ?, ?, ?)
"""

cursor.executemany(sql_insert, painters_df.values.tolist())
conn.commit()

print("Inserted successfully into painters.db")

#A Thống kê toàn cục
#1 Đếm tổng số họa sĩ đã được lưu trữ trong bảng.
cursor.execute("select count (*)from painters")
print("tổng số họa sĩ:", cursor.fetchone()[0])


#2 Hiển thị 5 dòng dữ liệu đầu tiên để kiểm tra cấu trúc và nội dung bảng.
print("\n5 dòng dữ liệu đầu tiên:")
cursor.execute("SELECT * FROM painters LIMIT 5")
for row in cursor.fetchall():
    print(row)

#3 Quốc tịch
print("\nThống kê số họa sĩ theo quốc tịch:")
cursor.execute("select distinct nationality from painters")
for row in cursor.fetchall():
    print("-", row[0])

#4 Hoạ sĩ tên bắt đầu bằng F
cursor.execute("select count(*) from painters where name like 'F%'")
for row in cursor.fetchall():
    print("\nSố họa sĩ có tên bắt đầu bằng chữ F:", row[0])

#5 Quốc tịch chưa French
cursor.execute("select name, nationality from painters where nationality != 'French'")
for row in cursor.fetchall():
    print("-",row)

#6 0 có quốc tịch
cursor.execute("select name from painters where nationality is null or nationality =' '")
for row in cursor.fetchall():
    print("-", row[0])

#7 có cả birth + death
print("\n7. Họa sĩ có cả năm sinh và năm mất:")
cursor.execute("""
select name from painters
where birth is not null and birth != '' 
and death is not null and death != ''
""")
for row in cursor.fetchall():
    print("-", row[0])

#8 tên chứa Fales
print("\n8. Họa sĩ có tên chứa 'Fales':")
cursor.execute("select name from painters where name like '%Fales%'")
for row in cursor.fetchall():
    print("-", row[0])  

#9 sắp xếp theo a-z
print("\n9. Họa sĩ sắp xếp theo tên A-Z:")
cursor.execute("select name from painters order by name asc")
for row in cursor.fetchall():
    print("-", row[0])

#10 nhóm theo quốc tịch
print("\n10. Thống kê số họa sĩ theo quốc tịch:")
cursor.execute("""
select nationality, count(*) 
from painters
group by nationality
order by count(*) desc
""")    

for row in cursor.fetchall():
    print(f"- {row[0]}: {row[1]} họa sĩ")

conn.close()
print("\nĐã đóng kết nối cơ sở dữ liệu.")