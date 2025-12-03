from pygments.formatters import HtmlFormatter
from selenium import webdriver
from selenium.webdriver.common.by import By     
import time
import pandas as pd
import re

d = pd.DataFrame ({'name': [], 'birth': [], 'death': [], 'nationality': []})

driver = webdriver.Chrome()

url = "https://en.wikipedia.org/wiki/Edvard_Munch"
driver.get(url)

time.sleep(2)

#ten
try:
    name = driver.find_element(By.TAG_NAME, "hl").text    
except:
    name = ""

#ngay sinh
try:
    birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
    birth = birth_element.text
    birth = re.tindall(r'[0-9]{1,2}'+r'\s'+r'[A-Za-z]+'+r'\s'+r'[0-9]{4}', birth)
except:
    birth = ""

#ngay mat
try:
    death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
    death = death_element.text
    death = re.findall(r'[0-9]{1,2}'+r'\s'+r'[A-Za-z]+'+r'\s'+r'[0-9]{4}', death)  
except:
    death = ""

#quoc tich
try:    
    nationality_element = driver.find_element(By.XPATH, "//th[text = 'nationality']/following-sibling::td")
    nationality = nationality_element.text
except:
    nationality = ""

#in thong tin
painter = {'name': name, 'birth': birth, 'death': death, 'nationality': nationality}
painter_df = pd.DataFrame([painter])
d = pd.concat([d, painter_df], ignore_index=True)   
print(d)

driver.quit()
