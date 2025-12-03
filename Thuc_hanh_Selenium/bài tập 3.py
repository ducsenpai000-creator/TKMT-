from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22P%22"
driver.get(url)

time.sleep(2)

ul_tags = driver.find_elements(By.XPATH, "//ul")    
print(len(ul_tags))

ul_painters = ul_tags[20]

li_tags = ul_painters.find_elements(By.TAG_NAME, "li")

ul_painters = ul_tags[20] 

li_tags = ul_painters.find_elements(By.TAG_NAME, "li")

links = [tags.find_element(By.TAG_NAME, "a").get_attribute("href") for tags in li_tags]

titles = [tags.find_element(By.TAG_NAME, "a").get_attribute("title") for tags in li_tags] 

for link in links:
    print(link) 

for title in titles:
    print(title)

driver.quit()