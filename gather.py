from os.path import join
from selenium import webdriver
import os
import urllib.request
import time
import datetime
from selenium.webdriver.chrome.options import Options
import random


chrome_options = Options()
chrome_options.add_argument('headless')
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument("disable-gpu")

def doScrollDown(whileSeconds, driver):
    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=whileSeconds)
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        if datetime.datetime.now() > end:
            break

header_n = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

def crawl(keywords):
    path = "https://www.google.com/search?q=" + keywords + "&newwindow=1&rlz=1C1CAFC_enKR908KR909&sxsrf=ALeKk01k_BlEDFe_0Pv51JmAEBgk0mT4SA:1600412339309&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj07OnHkPLrAhUiyosBHZvSBIUQ_AUoAXoECA4QAw&biw=1536&bih=754"
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options= chrome_options)
    driver.implicitly_wait(3)
    driver.get(path)
    driver.maximize_window()
    doScrollDown(2,driver=driver)
    time.sleep(1)

    counter = 0
    succounter = 0

    print(os.path)
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('data/' + keywords):
        os.makedirs('data/' + keywords)

    for x in driver.find_elements_by_class_name('rg_i.Q4LuWd'):
        counter = counter + 1
        print(counter)
        # 이미지 url
        img = x.get_attribute("data-src")
        if img is None:
            img = x.get_attribute("src")
        print(img)

        # 이미지 확장자
        imgtype = 'jpg'

        # 구글 이미지를 읽고 저장한다.

        try:
            raw_img = urllib.request.urlopen(img).read()
            File = open(os.path.join('data/' + keywords, keywords + "_" + str(counter) + "." + imgtype), "wb")
            File.write(raw_img)
            File.close()
            succounter = succounter + 1
        except:
            print('error')

    print(succounter, "succesfully downloaded")
    driver.close()

def listing_idol_group():
    
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options= chrome_options)
    path = 'https://ko.wikipedia.org/wiki/%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EC%95%84%EC%9D%B4%EB%8F%8C_%EA%B7%B8%EB%A3%B9_%EB%AA%A9%EB%A1%9D#%EA%B0%99%EC%9D%B4_%EB%B3%B4%EA%B8%B0'
    driver.get(path)

    idols ={}
    lista = driver.find_elements_by_xpath('//*[@id="mw-content-text"]/div[1]/table['+ str(6) +']/tbody/tr[*]/td[1]')
    listb = driver.find_elements_by_xpath('//*[@id="mw-content-text"]/div[1]/table['+ str(7) +']/tbody/tr[*]/td[1]|//*[@id="mw-content-text"]/div[1]/table['+ str(7) +']/tbody/tr[*]/td[2]')
    listc = driver.find_elements_by_xpath('//*[@id="mw-content-text"]/div[1]/table['+ str(8) +']/tbody/tr[*]/td[1]|//*[@id="mw-content-text"]/div[1]/table['+ str(8) +']/tbody/tr[*]/td[2]')

    def listing(idols,lista):
        for a in range(len(lista)):
            print(lista[a].text)
            idols[lista[a].text.split('\n')[0]] = ','.join(lista[a].text.split('\n')[1:])

        return idols

    idols = listing(idols,lista)
    
    def listingb(idols, listb):
        c = len(listb)
        for b in range(0,c,2):
            print(listb[b].text +" : "+ listb[b+1].text )
            idols[listb[b].text] = listb[b+1].text
        return idols
    
    idols = listingb(idols, listb)
    idols = listingb(idols, listc)
    
        
    def collect_member(idol):
        rs_idol={}
        path = 'https://www.google.com/search?q=' + idol +'+멤버'
            
        try:
            driver.get(path)
            members = driver.find_elements_by_xpath('/html/body/div[7]/div/div[7]/div/div/div/div/div[3]/div/div[2]/div/g-scrolling-carousel/div[1]/div/div[*]/div/div[*]/div/a/div[*]/div[*]/div/div[1]')

            list_tmp=[]   
            for member in members:
                list_tmp.append(member.text)
                
            rs_idol[idol]=','.join(list_tmp)

        except Exception as e:
            print(e)
            pass

        return rs_idol
    
    result =[]
    count = 0
    
    try:
        driver.close()
    except:
        pass
    
    for idol in range(len(idols.keys())):
        
        if count%5 ==0:
            driver = webdriver.Chrome('./chromedriver.exe', chrome_options= chrome_options)
        
        rs_idol = collect_member(list(idols.keys())[count])
        
        if list(rs_idol.values())[0] == '':
            print('정보 없음')
            pass
        else:
            result.append(rs_idol)
            print(rs_idol)

        count +=1

        driver.implicitly_wait(random.randint(3,5))
        
        if count %5==0:
            driver.close()


import json

result = json.dumps(result)


f = open("save.txt", 'w')
f.write(result)
f.close()
