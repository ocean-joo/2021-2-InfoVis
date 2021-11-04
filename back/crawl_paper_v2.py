import selenium
from selenium import webdriver
import time

def crawl(email, output) :
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-blink-features=AutomationControlled')

    # PROXY = "140.227.211.47:8080"
    # webdriver.DesiredCapabilities.CHROME['proxy'] = {
    #     "httpProxy": PROXY,
    #     "ftpProxy": PROXY,
    #     "sslProxy": PROXY,
    #     "proxyType": "MANUAL",
    # }

    url = "https://scholar.google.co.kr/scholar?q=" + email
    driver = webdriver.Chrome(executable_path='chromedriver', options=options)

    driver.get(url=url)
    f = open(output, 'w',encoding='UTF-16')

    paper_num = int(driver.find_element_by_css_selector("#gs_ab_md > div").text.split("(")[0][7:-2])
    print(paper_num)

    time.sleep(10)

    for i in range(0, int((paper_num)/10)+1) :
        if i == 0 :
            sub_url = url
        else :
            sub_url = url + "&start=" + str(i*10)
        sub_driver = webdriver.Chrome(executable_path='chromedriver', options=options)
        sub_driver.get(url=sub_url)
        driver.implicitly_wait(5)

        for paper_content in sub_driver.find_elements_by_css_selector("#gs_res_ccl_mid > div") :
            driver = webdriver.Chrome(executable_path='chromedriver', options=options)
            paper_name = paper_content.find_element_by_css_selector("h3").text
            id = paper_content.get_attribute("data-cid")
            p = paper_content.get_attribute("data-rp")
            bib_url = "https://scholar.google.co.kr/scholar?q="+email+"#d=gs_cit&u=%2Fscholar%3Fq%3Dinfo%3A"+id+"%3Ascholar.google.com%2F%26output%3Dcite%26scirp%3D"+p+"%26hl%3Dko"
            driver.get(bib_url)
            driver.implicitly_wait(5)

            try :
                journal = driver.find_element_by_css_selector("#gs_citt > table > tbody > tr:nth-child(1) > td > div > i").text
            except :
                journal = ""
            _apa = driver.find_element_by_css_selector("#gs_citt > table > tbody > tr:nth-child(1) > td > div").text
            
            author, journal = process_apa(_apa)
            print(_apa)
            f.write("%s+%s+%s\n" % (paper_name, author, journal))
            # driver.delete_all_cookies()
            driver.close()
            
        sub_driver.close()
        break

    f.close()

def process_apa(_apa) :
    split_apa = _apa.split("\"")
    return split_apa[0].strip(), split_apa[1].strip()

if __name__ == '__main__' :
    """
        Input: Email information for professor
        Output: Paper lists for specific professor (saved as csv format)
        TODO: Complete mechanism feeding email information to crawl function
        TODO: Error handling when specific email does not have paper at all.
    """
    email = "mkang@snu.ac.kr"
    path = "output/{}/{}.csv".format("snu", "강명주")
    crawl(email, path)