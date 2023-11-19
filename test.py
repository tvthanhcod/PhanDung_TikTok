# acc= open("data_test.txt",encoding="utf-8-sig").readlines()
# print(acc[0].strip())
# listoutput=[]
# for v,i in enumerate(acc):
#         # Tách chuỗi dữ liệu thành các phần riêng biệt
#         parts = i.split('|')

#         # Lấy phần đầu tiên và loại bỏ khoảng trắng thừa
#         first_part = parts[0].strip()
#         #Lấy tên người dùng bằng cách tách phần đầu tiên theo ký tự '@' và trích xuất phần tử thứ hai
#         username = first_part.split('@')[1]
#         listoutput.append(username)
#         print(username)
# with open('output.txt', 'w') as file:
#     # Ghi từng phần tử của mảng vào tệp tin, mỗi phần tử trên một dòng
#     for string in listoutput:
# #         file.write(string + '\n')
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
# # Adding argument to disable the AutomationControlled flag 
# chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
# # Exclude the collection of enable-automation switches 
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
# # Turn-off userAutomationExtension 
# chrome_options.add_experimental_option("useAutomationExtension", False) 
# driver = webdriver.Chrome(options=chrome_options)
# driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
# driver.get("https://www.tiktok.com/@sdfds")
#create chromeoptions instance
# https://www.tiktok.com/@@/sdfds323

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

     
# driver.close()

def getstatus(username):
        #create chromeoptions instance
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs",prefs)
    # options.add_argument('headless')
    # options.add_argument('window-size=1920x1080')
    # options.add_argument("disable-gpu")
    # options.add_argument("--no-sandbox")
    driver=webdriver.Chrome(options=options)
    url=f"https://www.tiktok.com/@{username}"
    driver.get(url)
    for i in range(15):
        print(f"lần tìm kiếm thứ: {i}")
        #Kiem tra xem phan tu follow co ton tai khong
        try:
            usertitle = WebDriverWait(driver,1 ).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-1h3j14u-DivFollowButtonWrapper")))
            print('tài khoản live')
            return 0
        except:
            try:
                usertitle=WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".css-1osbocj-DivErrorContainer")))
                print('tài khoản die')
                return 1
            except:
                pass
    print('tk không xác định')   
    return 2

print(getstatus('sdfds323'))