#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import time
import datetime

import selenium
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


# In[ ]:


#得到登入session，把原本的刪除串改後放回去
def change_id_cookie(driver , id_session):
    cookie = driver.get_cookie('ASP.NET_SessionId')
    if not cookie:
        print('No Cookie detect.')
        return
    elif cookie['value'] == id_session:
        return
    cookie['value'] = id_session
    driver.delete_cookie('ASP.NET_SessionId')
    driver.add_cookie(cookie)

def refresh_sessionID():
    with open('id_session.txt') as f:
        id_session = f.readline()
        f.close()
    
    options = ChromeOptions() 
    options.add_argument('--headless')
    user_agent = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    options.add_argument(user_agent)
    
    driver = webdriver.Chrome(options = options, service=Service())
    url = f'https://scr.cyc.org.tw/tp12.aspx?module=ind&files=ind'
    driver.get(url)
    
    change_id_cookie(driver, id_session)
    time.sleep(0.5)
    driver.refresh()
    try:
        if (driver.find_element(By.ID , value = 'lab_Name').text):
            print(driver.find_element(By.ID , value = 'lab_Name').text)
        else:
            print('SessionID expired.')
    except:
        driver.close()
        return
    driver.close()
    return driver.find_element(By.ID , value = 'lab_Name').text
    

def fetch_badminton():
    t = time.time()
    #得到明天的日期格式
    date = datetime.datetime.today() + datetime.timedelta(days = 1)
    date = date.strftime('%Y/%m/%d')
    
    #建立儲存資料的df
    df = pd.DataFrame(columns = ['運動中心' , '運動種類' , '場地' , '日期' , '時間'])
    
    #給定基本參數
    #website的aspx編碼
    websites = {'南港':'02',
                '汐止':'09',
                '內湖':'12'}
    
    #D分為1早上 2下午 3晚上
    Ds = [1,2,3]

    #讀取id_session，怎麼加密保護還沒想好
    with open('id_session.txt') as f:
        id_session = f.readline()
        f.close()
    
    #給瀏覽器的options增加user_agent的訊息
    options = ChromeOptions() 
    options.add_argument('--headless')
    user_agent = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    options.add_argument(user_agent)
    
    driver = webdriver.Chrome(options = options, service=Service())
    
    #df的index
    i = 0
    
    for k , v in websites.items():
        
        url = f'https://scr.cyc.org.tw/tp{v}.aspx?module=ind&files=ind'
        driver.get(url)
        
        change_id_cookie(driver, id_session)
        time.sleep(0.5)
        D = 1 #先給定1要有個初始網站爬所有可訂日期
        url_book = f'https://scr.cyc.org.tw/tp{v}.aspx?module=net_booking&files=booking_place&StepFlag=2&PT=1&D={date}&D2={D}'
        driver.get(url_book)

        sport_type = driver.find_element(by=By.ID , value = 'ContentPlaceHolder1_Step2_SportType_lab').text

        dates_list = []
        for d in driver.find_element(By.ID , value = 'ContentPlaceHolder1_Date_Step2_lab').find_elements(By.CSS_SELECTOR , value = 'option'):
            dates_list.append(d.get_property('value'))

        for d in dates_list:

            for D in Ds:
                url_book = f'https://scr.cyc.org.tw/tp{v}.aspx?module=net_booking&files=booking_place&StepFlag=2&PT=1&D={d}&D2={D}'
                driver.get(url_book)
                book_table = driver.find_element(By.XPATH , value = '/html/body/div/table[1]/tbody/tr[3]/td/div/form/table/tbody/tr/td/span/div/table/tbody/tr[2]/td/span/table')
                for _ in book_table.find_elements(By.CSS_SELECTOR , value = 'img'):
                    if 'confirm' in _.get_attribute('onclick'):
                        available = _.get_attribute('onclick').split("'")[1].split('「')[1].split('」')[0]
                        time_ = available.split()[-1]
                        area = ''.join(available.split()[:-1])
                        df.loc[i] = [k , sport_type , area , d , time_]
                        i+=1

    driver.close()
    print(f'Finished! Spend time : {time.time()-t:.2f} s')
    
    date = date.replace('/','')
    df.to_csv(f'./歷史資料/{date}_羽球.csv', index=False) #存歷史資料用
    df.to_excel(f'./歷史資料/{date}_羽球.xlsx', index=False) #存歷史資料用
    df.to_json('badminton.json' , orient='records' , force_ascii=False) #API用
    

