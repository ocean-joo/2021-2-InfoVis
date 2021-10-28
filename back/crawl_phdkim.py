import selenium
from selenium import webdriver
import time

CRAWL = 'kaist' # snu, postech, kaist, yonsei, korea

url_list = {'postech': "https://phdkim.net/professor/search/department/2274/",
                'snu': "",
                'kaist':"https://phdkim.net/professor/search/department/1241/",
                'yonsei':"https://phdkim.net/professor/search/department/1641/",
                'korea':"https://phdkim.net/professor/search/department/2252/"}

output_list = {'postech': "output/postech_phdkim.csv",
                'snu': "output/snu_phdkim.csv",
                'kaist':"output/kaist_phdkim.csv",
                'yonsei':"output/yonsei_phdkim.csv",
                'korea':"output/korea_phdkim.csv"}

def crawl(path, output) :
    driver = webdriver.Chrome(executable_path='chromedriver')
    driver.get(url=path)
    f = open(output, 'w')

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

            print("[Crawled] Name: %s,. Homepage: %s\n" % (name, homepage))
            f.write("%s,%s\n" % ( name, homepage))

    driver.close()
    f.close()

if __name__ == '__main__' :
    crawl(url_list[CRAWL], output_list[CRAWL])

