import bs4, time
import requests
from requests.auth import HTTPProxyAuth

CRAWL_SCHOOL = 'snu' # snu, postech, kaist, yonsei, korea

def crawl(email, output) :
    header =  {'User-Agent': 'Mozilla/5.0'}
    url = "https://scholar.google.co.kr/scholar?q=" + email

    result = requests.get(url, headers=header)
    soup = bs4.BeautifulSoup(result.content, 'html.parser')

    f = open(output, 'w',encoding='UTF-16')
    paper_num = int(soup.select_one("#gs_ab_md > div").text.split("(")[0][7:-2])
    time.sleep(5)

    for i in range(0, int((paper_num)/10)+1) :
        if i == 0 :
            sub_url = url
        else :
            sub_url = url + "&start=" + str(i*10)

        sub_result = requests.get(sub_url, headers=header)
        sub_soup = bs4.BeautifulSoup(sub_result.content, 'html.parser')

        for paper_content in sub_soup.select("#gs_res_ccl_mid > div") :
            paper_name = paper_content.select_one("h3").text
            link = paper_content.select_one("h3 > a").get("href")

            print("[CRAWLED] %s, %s\n" % (paper_name, link))
            f.write("%s+%s\n" % (paper_name, link))

    f.close()


def process_apa(_apa) :
    split_apa = _apa.split("\"")
    if split_apa[0].strip() == "" :
        return split_apa[1].strip()
    else :
        return split_apa[0].strip()


if __name__ == '__main__' :
    """
        Input: Email information for professor
        Output: Paper lists for specific professor (saved as csv format)
        TODO: Complete mechanism feeding email information to crawl function
        TODO: Error handling when specific email does not have paper at all.
    """
    
    meta_path_dict =  {'postech': "output/postech_homepage.csv",
                        'snu': "output/snu_homepage.csv",
                        'kaist':"output/kaist_homepage.csv",
                        'yonsei':"output/yousei_homepage.csv",
                        'korea':"output/korea_homepage.csv"}

    meta = meta_path_dict[CRAWL_SCHOOL]
    
    with open(meta, 'r') as f : 
        lines = f.readlines()
        for line in lines :
            name, email, _ = line.split(",")
            path = "output/{}_{}.csv".format(CRAWL_SCHOOL, name)

            crawl(email, path) 