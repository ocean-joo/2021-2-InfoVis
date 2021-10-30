import selenium
from selenium import webdriver
import time

SCROLL_PAUSE_SEC = 2

def crawl(email, output) :
    url = "https://scholar.google.co.kr/scholar?q=" + email
    driver = webdriver.Chrome(executable_path='chromedriver')
    driver.get(url=url)
    f = open(output, 'w',encoding='UTF-16')

    paper_num = int(driver.find_element_by_css_selector("#gs_ab_md > div").text.split("(")[0][7:-2])
    print(paper_num)

    for i in range(0, int(paper_num/10)) :
        if i == 0 :
            sub_url = url
        else :
            sub_url = url + "&start=" + str(i*10)
        sub_driver = webdriver.Chrome(executable_path='chromedriver')
        sub_driver.get(url=sub_url)

        for paper_content in sub_driver.find_elements_by_css_selector("#gs_res_ccl_mid > div") :
            paper_name = paper_content.find_element_by_css_selector("h3").text

            print("[Crawled]:", paper_name)
            f.write("\"%s\"\n" % (paper_name))

    driver.close()
    f.close()

if __name__ == '__main__' :
    """
        Input: Email information for professor
        Output: Paper lists for specific professor (saved as csv format)
        TODO: Complete mechanism feeding email information to crawl function
        TODO: Error handling when specific email does not have paper at all.
    """
    email = "mkang@snu.ac.kr"
    path = "output/{}_{}.csv".format("snu", "강명주")
    crawl(email, path)