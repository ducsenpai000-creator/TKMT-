from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re

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

    try:
        name = driver.find_element(By.TAG_NAME, "h1").text
    except:
        name = ""

    try:
        birth_text = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td").text
        birth_match = re.findall(r'\d{1,2}\s[A-Za-z]+\s\d{4}|\d{4}', birth_text)
        birth = birth_match[0] if birth_match else ""
    except:
        birth = ""

    try:
        death_text = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td").text
        death_match = re.findall(r'\d{1,2}\s[A-Za-z]+\s\d{4}|\d{4}', death_text)
        death = death_match[0] if death_match else ""
    except:
        death = ""

    try:
        citizen = driver.find_element(By.XPATH, "//th[text()='nationality']/following-sibling::td").text
    except:
        citizen = ""

    painters_df.loc[len(painters_df)] = [name, birth, death, citizen]

driver.quit()

painters_df.to_excel("painters_info.xlsx", index=False)
print("Data saved successfully")
