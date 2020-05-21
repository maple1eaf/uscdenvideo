import requests
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import json
import sys

SLEEP_TIME = 5

def getCourseHashId(driver, course_id):
    try:
        header = driver.find_element_by_tag_name('header')
        course_menu_button = header.find_element_by_class_name('d2l-navigation-s-course-menu')
        course_menu_button.click()
        time.sleep(SLEEP_TIME)

        course_selector = driver.find_element_by_id('courseSelectorId')
        courses_a = course_selector.find_elements_by_tag_name('a')

        target_course_a = None
        for course_a in courses_a:
            if course_id in course_a.text.lower():
                target_course_a = course_a
                break
        
        target_course_home_url = target_course_a.get_attribute('href')
        l1 = target_course_home_url.split('/')
        cid = None
        for i in l1:
            try:
                cid = int(i)
            except:
                continue
        return cid
    except:
        return None

def getVideoUrls(driver, url_content):
    driver.get(url_content)
    time.sleep(SLEEP_TIME)

    toc = driver.find_element_by_id('TreeItemTOC')
    toc.click()
    time.sleep(SLEEP_TIME)

    link_list = driver.find_elements_by_class_name('d2l-link')
    filtered_links = []
    for link in link_list:
        href_str = link.get_attribute('href')
        if "viewContent" in href_str:
            filtered_links.append(href_str)

    return filtered_links

def getM3u8(driver, urlWebContainVideo):
    """
    parse webpage that contains video
    """
    try:
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
        
        item = {
            "foldername": folderName,
            "filetitle": fileTitle,
            "url": urlFileAWS
        }
        return item
    except:
        return None

def main():
    # load urls
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    userName = config['username']
    password = config['password']
    course_id = str(config['course_id']).lower()
    print(course_id)

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

    cid = getCourseHashId(driver, course_id)
    if cid == None:
        print('wrong course_id or the course does not exist in your course list.')
        print('course_id should be as "csci123".')
        sys.exit(0)
    url_content = "https://courses.uscden.net/d2l/le/content/%s/Home" % (cid)

    urlWebContainVideos = getVideoUrls(driver, url_content)
    # print('\n', urlWebContainVideos)

    urlDirectVideos = []
    for urlWebContainVideo in urlWebContainVideos:
        item = getM3u8(driver, urlWebContainVideo)
        if item != None:
            urlDirectVideos.append(item)

    print(urlDirectVideos)

    driver.close()

    with open('urlOfVideos.json', 'w', encoding='utf-8') as f:
        json.dump(urlDirectVideos, f)

if __name__ == "__main__":
    main()
