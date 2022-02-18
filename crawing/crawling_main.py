from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib import request
import time
import os

search_word = input("입력:")

driver = webdriver.Chrome('C:\Temp\chromedriver.exe')
driver.implicitly_wait(3)

driver.get('https://www.google.co.kr/imghp?hl=ko&ogbl')
elem = driver.find_element_by_name('q')
elem.send_keys(search_word)
elem.send_keys(Keys.RETURN)
time.sleep(1)

scroll_height = driver.execute_script("return document.body.scrollHeight")
print(scroll_height)

while True:
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(1)

    new_scroll_height = driver.execute_script("return document.body.scrollHeight")

    if scroll_height == new_scroll_height:
        try:
            driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div[1]/div[2]/div[2]/input').click()
        except:
            break
    scroll_height = new_scroll_height
print("스크롤 완료")

try:
    if not os.path.exists(search_word):
        os.makedirs('C:/crawling/img/'+search_word)
except Exception as err:
    print(err)
    pass

images = driver.find_elements_by_css_selector('img.rg_i.Q4LuWd')
print(f'images count :{len(images)}')

cnt =0
for image in images:

    try:
        image.click()
        time.sleep(1)

        xpath_='//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img'
        bigImage_url = driver.find_element_by_xpath(xpath_).get_attribute('src')
        file_ext = bigImage_url.split('.')[-1]

        if file_ext in ['jpg','jpeg','png','gif','bmp']:
            filename = str(time.time())+'_'+os.path.basename(bigImage_url)

            request.urlretrieve(bigImage_url,'C:/crawling/img/'+search_word+'/'+filename)

            cnt += 1

            if cnt % 5 ==0:
                print(f'검색어 "{search_word}"의 이미지 {cnt}장 저장 중...')

        else:
            filename = str(time.time()) + '_.jpg'
            request.urlretrieve(bigImage_url,'C:/crawling/img/'+search_word+'/'+filename)

            cnt += 1

    except Exception as err:
        print(err)

    if cnt == 4:
        break
print(f'검색어"{search_word}"의 이미지 저장 완료!!')

driver.close()


