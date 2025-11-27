from pygments.formatters.html import webify
from selenium import webdriver
from selenium.webdriver.common.by import By 
import time
import re
import pandas as pd

# tai? noi chua link va tao datafarme rong
all_links = []
d = pd.DataFrame({
    'name': [], 'birth': [], 'death': [], 'nationality': []
})

for i in range(70, 71):
    driver = webdriver.Chrome()
    url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22" + chr(i) + "%22"
    try:
        # mo trang
        driver.get(url)
        
        # cho trang load
        time.sleep(2)
        
        # <<< PHẦN ĐIỀU CHỈNH QUAN TRỌNG NHẤT NẰM Ở ĐÂY >>>
        
        # 1. Lấy TẤT CẢ thẻ ul trong khu vực nội dung chính (id="mw-content-text")
        ul_tags_in_content = driver.find_elements(By.XPATH, '//*[@id="mw-content-text"]//ul')
        
        # 2. CHỌN thẻ ul THỨ HAI ([1]) - đây chính là danh sách họa sĩ
        ul_painters = ul_tags_in_content[1]
        
        li_tags = ul_painters.find_elements(By.TAG_NAME, "li")
        
        # 4. ĐẾM VÀ IN RA SỐ LƯỢNG
        so_luong_tac_gia = len(li_tags)
        print(f"✅ Trang {chr(i)}: Số lượng tác giả trong danh sách chính là: {so_luong_tac_gia}")
        # <<< KẾT THÚC ĐIỀU CHỈNH >>>
        
        # lay tat ca the li trong the ul
        li_tags = ul_painters.find_elements(By.TAG_NAME, "li")
        
        # tao danh sach chua link
        link = [tag.find_element(By.TAG_NAME, "a").get_attribute("href") for tag in li_tags]
        for x in link:
            all_links.append(x)
            
    except IndexError:
        print(f"ERROR! Không tìm thấy đủ 2 thẻ <ul> trong nội dung chính của trang {chr(i)}.")
    except Exception as e:
        print(f"ERROR! Lỗi chung khi xử lý trang {chr(i)}: {e}")
    
    #dong trinh duyet
    driver.quit()

#lay thong tin cua tung hoa si
count = 0
for link in all_links:
    if(count > 3):
        break
    count+=1
    
    print(link)
    try:
        # khoi tao trinh duyet
        driver = webdriver.Chrome()
        #mo trang
        url = link
        driver.get(url)
        time.sleep(2)  #cho trang load
        
        # Lay ten hoa si (Giữ nguyên)
        try:
            name = driver.find_element(By.TAG_NAME, "h1").text
        except:
            name = ""

        # Lay ngay sinh (Không dùng re.findall)
        try:
            birth_element = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td")
            birth = birth_element.text  # Giữ nguyên toàn bộ chuỗi text
        except:
            birth = ""

        # Lay ngay mat (Không dùng re.findall)
        try:
            death_element = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td")
            death = death_element.text  # Giữ nguyên toàn bộ chuỗi text
        except:
            death = ""

        # Lay quoc tich (Giữ nguyên)
        try:
            nationality_element = driver.find_element(By.XPATH, "//th[text()='Nationality']/following-sibling::td")
            nationality = nationality_element.text
        except:
            nationality = ""
        
        #tao dictionnary cua hoa sy
        painter = {'name':name, 'birth':birth, 'death':death, 'nationality':nationality}

        #chuyen thanh dataframe
        painter_df = pd.DataFrame([painter])

        #them thong tin
        d = pd.concat([d, painter_df], ignore_index=True)
        
        driver.quit()
    except:
        pass
# IN thong tin
print(d)
filename = "Painters.xlsx"
#save to excel
d.to_excel(filename)
print("datafame is written to excel file successfully.")