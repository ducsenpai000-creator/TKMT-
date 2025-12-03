from builtins import range
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

for i in range(65, 91):
    url = f"https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22{chr(i)}%22"
    try:
        driver.get(url)
        time.sleep(3)

        ul_tags = driver.find_elements(By.TAG_NAME, "//ul")
        print(len(ul_tags))
        ul_painters = ul_tags[20]
        li_tags = ul_painters.find_elements(By.TAG_NAME, "li")

        titles = [tags.find_element(By.TAG_NAME, "a").get_attribute("title") for tags in li_tags]

        for title in titles:
            print(title)

    except:
        print("error")
    
driver.quit()
