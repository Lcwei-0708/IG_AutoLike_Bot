import sys
import time
import json
import pandas
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys as Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 設定使用者資料
headers = {"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71"}

# 保持視窗打開
option = webdriver.EdgeOptions()
option.add_experimental_option('detach', True)

# 設定瀏覽器
driver = webdriver.Edge('D:/Webdriver/msedgedriver.exe',options = option)   

# 視窗最大化
driver.maximize_window()

# 帳號清單
email_list = ['TanjiroMizu01@gmail.com',
              'TanjiroMizu02@gmail.com',
              'TanjiroMizu03@gmail.com',
              'TanjiroMizu04@gmail.com',
              'TanjiroMizu05@gmail.com',
              'TanjiroMizu06@gmail.com',
              'TanjiroMizu07@gmail.com',              
              'TanjiroMizu08@gmail.com',
              'TanjiroMizu09@gmail.com',
              'TanjiroMizu10@gmail.com']

# 密碼清單
password_list = ['Mizu01_Tanjiro',
                 'Mizu02_Tanjiro',
                 'Mizu03_Tanjiro',
                 'Mizu04_Tanjiro',
                 'Mizu05_Tanjiro',
                 'Mizu06_Tanjiro',
                 'Mizu07_Tanjiro',              
                 'Mizu08_Tanjiro',
                 'Mizu09_Tanjiro',
                 'Mizu10_Tanjiro']

# 貼文網址清單
posts_list = ['https://www.instagram.com/p/CgghuRgpH-j/',
              'https://www.instagram.com/p/Cgd8674DDXY/',
              'https://www.instagram.com/p/CgbYJxJg36L/',
              'https://www.instagram.com/p/CgYzT2JMNfZ/',
              'https://www.instagram.com/p/CgVJ7FqPM-A/',
              'https://www.instagram.com/p/CgTpvrPM2hN/']

# 隨機選擇一組帳號
user_number = random.randint(0,len(email_list)-1)

#貼文網址
post_url = ''

# 登入IG帳號
def Login_IG():    
    
    # 讀取IG網頁
    driver.get('https://www.instagram.com/')
    
    # 等待輸入帳號欄位出現並且抓取XPath
    email = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="loginForm"]/div/div[1]/div/label/input'))
        )
    
    # 輸入帳號
    email.send_keys(email_list[user_number])
    
    # 等待1~3秒
    time.sleep(random.randint(1,3))
    
    # 等待輸入密碼欄位出現並且抓取XPath
    password = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="loginForm"]/div/div[2]/div/label/input'))
        )
    
    # 輸入密碼
    password.send_keys(password_list[user_number])
    
    # 等待1~3秒
    time.sleep(random.randint(1,3))
    
    # 送出
    password.submit()
    
    # 等待5~10秒
    time.sleep(random.randrange(5,10))
    
# 貼文按讚    
def Search_Posts():

    next_post = True
    
    while next_post:  
        
        #讓使用者輸入貼文網址
        post_url = str(input('請輸入貼文網址：'))
        
        #判斷網址是否正確
        if 'https://www.instagram.com/p/' in post_url:
            
            # 前往指定貼文
            driver.get(post_url)
            
            # 抓取愛心按鈕XPath
            like = WebDriverWait(driver,10).until(
                    EC.presence_of_all_elements_located(((By.CSS_SELECTOR,'span[class ="_aamw"]')))
                ) 
            
            # 等待3~5秒
            time.sleep(random.randint(3,5))
            
            #判斷是否已經按過讚
            if like[0].find_elements_by_css_selector('svg')[0].get_attribute('aria-label') == '讚':
                
                # 點擊愛心
                like[0].click()
                
                #等待1~3秒            
                time.sleep(random.randint(1,3))
                
                # 重新抓取愛心按鈕XPath
                like = WebDriverWait(driver,10).until(
                        EC.presence_of_all_elements_located(((By.CSS_SELECTOR,'span[class ="_aamw"]')))
                    ) 
                
                #判斷是否已按讚
                if like[0].find_elements_by_css_selector('svg')[0].get_attribute('aria-label') == '收回讚':
                    print('已成功按讚！')                
                    next_post = input('是否要繼續（Y/N）：')
                    
                    #判斷是否繼續下一篇貼文
                    if next_post == 'Y':
                        next_post = True
                        
                    elif next_post == 'N':
                        next_post = False
                        
                    else :
                        print('請輸入 Y 或 N')
                        next_post = input('是否要繼續（Y/N）：')
                        
                else :
                    print('按讚失敗！')
                    next_post = input('是否要繼續（Y/N）：')
                    
                    #判斷是否繼續下一篇貼文
                    if next_post == 'Y':
                        next_post = True
                        
                    elif next_post == 'N':
                        next_post = False
                        
                    else :
                        print('請輸入 Y 或 N')
                        next_post = input('是否要繼續（Y/N）：')
                
            elif like[0].find_elements_by_css_selector('svg')[0].get_attribute('aria-label') == '收回讚':
                print('此貼文已經按過讚！')
                next_post = input('是否要繼續（Y/N）：')
                
                #判斷是否繼續下一篇貼文
                if next_post == 'Y':
                    next_post = True
                    
                elif next_post == 'N':
                    next_post = False
                    
                else :
                    print('請輸入 Y 或 N')
                    next_post = input('是否要繼續（Y/N）：')
                    
            else :
                print(like[0].find_elements_by_css_selector('svg')[0].get_attribute('aria-label'))
                next_post = False
        else :
            print('請輸入正確的貼文網址')
            Search_Posts()
            break
        
# 嘗試執行
try:
    Login_IG()
    Search_Posts()

# 最後必定執行
finally:
    
    # 關閉瀏覽器
    driver.quit()
    print('已關閉瀏覽器')
    