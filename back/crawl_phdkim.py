import selenium
from selenium import webdriver
import time

SCROLL_PAUSE_SEC = 2

AI_url_list = {'postech': "https://phdkim.net/professor/search/department/2274/?q=postech",
                }

output_list = {'postech': "output/postech_phdkim.csv",
                }

driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url=AI_url_list['postech'])
f = open(output_list['postech'], 'w')

profs_element = driver.find_elements_by_class_name("search-result-list")

for prof_element in profs_element :
    for prof in prof_element.find_elements_by_class_name("item") :
        sub_driver = webdriver.Chrome(executable_path='chromedriver')

        name = prof.find_element_by_css_selector("a > div > p.name").text
        link = prof.find_element_by_css_selector("a").get_attribute("href")
        
        sub_driver.get(url=link)

        try :
            homepage = sub_driver.find_element_by_css_selector("body > div > div.container > div > div.professor-profile-area.js-professor-profile-area > div.professor-profile > p.site > a").text
        except :
            homepage = ""

        sub_driver.close()

        print("[Crawled]:", name, homepage)
        f.write("%s,%s\n" % ( name, homepage))

driver.close()
f.close()