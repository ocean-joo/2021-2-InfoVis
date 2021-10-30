import selenium
from selenium import webdriver
import time

SCROLL_PAUSE_SEC = 2
CRAWL = 'kaist' # snu, postech, kaist, yonsei, korea

url_list = {'postech': "http://ai.postech.ac.kr/sub020101",
                'snu': "https://gsai.snu.ac.kr/ko/portfolio",
                'kaist':"https://gsai.kaist.ac.kr/people/?lang=ko",
                'yonsei':"",
                'korea':""}

output_list = {'postech': "output/postech_homepage.csv",
                'snu': "output/snu_homepage.csv",
                'kaist':"output/kaist_homepage.csv",
                'yonsei':"output/yousei_homepage.csv",
                'korea':"output/korea_homepage.csv"}

def snu_crawl(path, output) :
    driver = webdriver.Chrome(executable_path='chromedriver')
    driver.get(url=path)
    f = open(output, 'w')

    # Scroll down to bottom
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_SEC)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    profs_element = driver.find_element_by_css_selector("#lc_content")

    for prof in profs_element.find_elements_by_class_name("d0") :
        name = prof.find_element_by_css_selector("dl > dt > a").text
        email = prof.find_element_by_css_selector("dl > dd > ul > li.l3 > a").text
        try :
            homepage = prof.find_element_by_css_selector("dl > dd > ul > li.l4 > a").text
        except :
            homepage = ""

        print("[Crawled]:", name, email, homepage)
        f.write("%s,%s,%s\n" % ( name, email, homepage))

    driver.close()
    f.close()

def postech_crawl(path, output) :
    PROXY = "117.102.78.42:8080"
    webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY,
        "proxyType": "MANUAL",
    }

    driver = webdriver.Chrome(executable_path='chromedriver')
    driver.get(url=path)

    f = open(output, 'w')

    profs_section = driver.find_elements_by_class_name("new-list3")

    for profs_element in profs_section.find_elements_by_css_selector("li") :
        for prof in profs_element.find_elements_by_css_selector("d0") :
            name = prof.find_element_by_css_selector("div.list-txt > strong").text
            try :
                homepage = prof.find_element_by_css_selector("div.list-txt > strong > img.homepage_class").get_attribute("href")
            except :
                homepage = ""

            print("[Crawled]:", name, homepage)
            f.write("%s,%s\n" % ( name, homepage))

    driver.close()
    f.close()

def kaist_crawl(path, output) :
    driver = webdriver.Chrome(executable_path='chromedriver')
    driver.get(url=path)
    driver.implicitly_wait(3)
    f = open(output, 'w')
    
    profs_section = driver.find_element_by_class_name("vc_tta-panel-body")

    for prof in profs_section.find_elements_by_css_selector("div.wpb_text_column.wpb_content_element") :
        name = prof.find_element_by_css_selector("div > div > div > p:nth-child(1) > strong").text
        # email = prof.find_element_by_css_selector("div > div > div > p:nth-child(2) > strong:nth-child(7)").text
        content = prof.find_element_by_css_selector("div > div > div > p:nth-child(2)").text
        email_line = content.split("\n")[3]
        email = email_line[6:]
        try :
            homepage = prof.find_element_by_css_selector("div > div > p:nth-child(2) > span > a").get_attribute("href")
        except :
            homepage = ""
        
        print("[Crawled]:", name,  email, homepage)
        f.write("%s,%s,%s\n" % ( name, email, homepage))

    driver.close()
    f.close()

def yonsei_crawl(path, output) :
    pass

def korea_crawl(path, output) :
    pass


func_list = {'postech': postech_crawl,
                'snu': snu_crawl,
                'kaist':kaist_crawl,
                'yonsei':yonsei_crawl,
                'korea':korea_crawl}

if __name__ == '__main__' :
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    func = func_list[CRAWL]
    func(url_list[CRAWL], output_list[CRAWL])