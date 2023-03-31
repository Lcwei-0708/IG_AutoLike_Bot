import time
import random
import maskpass
import warnings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys as Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# 讓棄用警告不顯示
warnings.filterwarnings('ignore',category = DeprecationWarning)

# 設定使用者資料
headers = {"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71"}

option = webdriver.EdgeOptions()
option.add_experimental_option('excludeSwitches', ['enable-logging'])
option.use_chromium = True

# 讓瀏覽器在背景執行
#option.add_argument('--headless')

# 設定瀏覽器
driver = webdriver.Edge(EdgeChromiumDriverManager().install(),options = option)

# 讀取IG網頁
driver.get('https://www.instagram.com/')

# 貼文網址
post_url = ''

# IG帳號
input_email = ''

# IG密碼
input_password = ''

# 登入IG帳號
def Login_IG():   
    
    while True:
        print('請輸入要登入的IG帳號')
        
        # 等待輸入帳號欄位出現並且抓取XPath
        email = WebDriverWait(driver,10).until(
                EC.presence_of_all_elements_located(((By.CSS_SELECTOR,'input[class ="_2hvTZ pexuQ zyHYP"]')))
            )[0]
        
        # 等待輸入密碼欄位出現並且抓取XPath
        password = WebDriverWait(driver,10).until(
                EC.presence_of_all_elements_located(((By.CSS_SELECTOR,'input[class ="_2hvTZ pexuQ zyHYP"]')))
            )[1]
        
        input_email = input('帳號：')
        input_password = maskpass.askpass(prompt="密碼：", mask="*")
 
        # 輸入帳號
        email.send_keys(input_email)
        
        # 等待1~3秒
        time.sleep(random.randint(1,3))
        
        # 輸入密碼
        password.send_keys(input_password)
        
        # 等待1~3秒
        time.sleep(random.randint(1,3))
        
        # 送出
        password.submit()
        
        try :
            
            # 讀取登入錯誤訊息欄位
            login_mistake = WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div[2]/p'))
                )            
            print(login_mistake.text,'\n')   
            driver.refresh()            
        
        except Exception as e:
            print('登入成功')
            
            # 等待3~5秒
            time.sleep(random.randint(3,5))
            break
        
#登出IG帳號
def Logout_IG():
    
    # 讀取用戶頭像按鈕並點擊
    user = WebDriverWait(driver,10).until(
            EC.presence_of_all_elements_located(((By.CSS_SELECTOR,'span[class ="_aa8h _aa8i"]')))
        )[0].click()
    
    # 等待1~3秒
    time.sleep(random.randint(1,3))
    
    # 讀取登出按鈕並點擊
    logout = WebDriverWait(driver,10).until(
            EC.presence_of_all_elements_located(((By.XPATH,'/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[2]/div[2]/div[2]/div[2]/div/div/div/div/div/div')))
        )[0].click()
    
    try :
        
        # 等待輸入帳號欄位出現並且抓取XPath
        email = WebDriverWait(driver,10).until(
                EC.presence_of_all_elements_located(((By.CSS_SELECTOR,'input[class ="_2hvTZ pexuQ zyHYP"]')))
            )
                        
        print('登出成功')
    
    except Exception as e:
        print('登出失敗')
    
    # 等待3秒  
    time.sleep(3)
    
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
    Logout_IG()
    
    # 關閉瀏覽器
    driver.quit()
    print('已關閉瀏覽器')
