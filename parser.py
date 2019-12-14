import requests
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import json

SLEEP_TIME = 5

# load urls
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

userName = config['username']
password = config['password']
urlWebContainVideos = config['urls']
print(urlWebContainVideos)

# get cookies
chrome_options = webdriver.ChromeOptions()
# headless mode
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://courses.uscden.net/d2l/login')
time.sleep(SLEEP_TIME)

driver.find_element_by_id('userName').send_keys(userName)
driver.find_element_by_id('password').send_keys(password, Keys.ENTER)
cookies = driver.get_cookies()
# print(cookies)

for cookie in cookies:
    driver.add_cookie(cookie)
# time.sleep(SLEEP_TIME)

def getM3u8(urlWebContainVideo):
    """
    parse webpage that contains video
    """
    if urlWebContainVideo == '':
        return ''

    driver.get(urlWebContainVideo)
    time.sleep(SLEEP_TIME)

    # with open("dev_sth/h1.html", "w") as f:
    #     f.write(driver.page_source)
    fileTitle = driver.title
    print("fileTitle:",fileTitle)

    folderName = driver.find_element_by_xpath('//ol[@aria-labelledby]/li[2]/a').get_attribute("innerHTML")
    print("folderName:",folderName)

    iframe_inner_html = driver.find_element_by_tag_name('iframe').get_attribute('src')
    # print("iframe_inner_html:",iframe_inner_html)

    driver.get(iframe_inner_html)
    time.sleep(SLEEP_TIME)

    # with open("iframe.html", "w") as f:
    #     f.write(driver.page_source)

    a_doplayer_onclick = driver.find_element_by_xpath("//a[contains(@onclick,'doPlayer')]").get_attribute('onclick')
    # print(a_doplayer_onclick)

    strRemovedoPlayer = a_doplayer_onclick.split('(')[1]
    strRemoveSecondThird = strRemovedoPlayer.split(',')[0]
    pieces = strRemoveSecondThird[1:-1].split('/')
    urlFileAWS = 'https://denawswz.uscden.net/aws/_definst_/smil:amazons3/gwz/' + pieces[0] + '/' + pieces[0] + '.smil/playlist.m3u8'
    print('urlFileAWS:', urlFileAWS)

    time.sleep(SLEEP_TIME)
    return (folderName, fileTitle, urlFileAWS)

urlDirectVideos = []
for urlWebContainVideo in urlWebContainVideos:
    fn, ft, url = getM3u8(urlWebContainVideo)
    item = {
        "foldername": fn,
        "filetitle": ft,
        "url": url
    }
    urlDirectVideos.append(item)

print(urlDirectVideos)

driver.close()

with open('urlOfVideos.json', 'w', encoding='utf-8') as f:
    json.dump(urlDirectVideos, f)
