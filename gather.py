from selenium import webdriver
import os
import urllib.request
import time
import datetime
from selenium.webdriver.chrome.options import Options

del chrome_options

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
    
    path = 'https://en.m.wikipedia.org/wiki/List_of_South_Korean_idol_groups_(2010s)'

    driver = webdriver.Chrome('./chromedriver.exe', chrome_options= chrome_options)
    driver.get(path)
    
    lista = driver.find_elements_by_xpath('/html/body/div[1]/div/main/div[3]/div[1]/div/section[*]/div/ul/li[*]/a')
    
    for a in lista:
        print(a.text)

    driver.close()
    
    
    
    driver.implicitly_wait(3)

    idols =[]
    lista = driver.find_elements_by_xpath('//*[@id="mw-content-text"]/div[1]/table['+ str(6) +']/tbody/tr[*]/td[1]/p')
    listb = driver.find_elements_by_xpath('//*[@id="mw-content-text"]/div[1]/table['+ str(7) +']/tbody/tr[*]/td[2]')
    listc = driver.find_elements_by_xpath('//*[@id="mw-content-text"]/div[1]/table['+ str(8) +']/tbody/tr[*]/td[2]')

    for a in lista:
        idols.append(a.text.strip('(').strip(')'))
        print(a.text.strip('(').strip(')'))
    for b in listb:
        idols.append(b.text.strip('(').strip(')'))
        print(b.text.strip('(').strip(')'))
    
    for c in listc:
        idols.append(c.text.strip('(').strip(')'))
        print(c.text.strip('(').strip(')'))

    driver.close()

    len(idols) # 337그룹
    idols[2]

    pass