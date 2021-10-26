import selenium
from selenium import webdriver
import time

SCROLL_PAUSE_SEC = 2

AI_url_list = {'SNU': "https://gsai.snu.ac.kr/ko/portfolio",
                }

output_list = {'SNU': "output/snu_homepage.csv",
                }

driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url=AI_url_list['SNU'])
f = open(output_list['SNU'], 'w')

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
    try :
        homepage = prof.find_element_by_css_selector("dl > dd > ul > li.l4 > a").text
    except :
        homepage = ""

    print("[Crawled]:", name, homepage)
    f.write("%s,%s\n" % ( name, homepage))

driver.close()
f.close()