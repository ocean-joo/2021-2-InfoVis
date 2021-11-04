import bs4, requests
import time

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
            id = paper_content["data-cid"]
            p = paper_content["data-rp"]

            bib_url = "https://scholar.google.co.kr/scholar?q="+email+"#d=gs_cit&u=%2Fscholar%3Fq%3Dinfo%3A"+id+"%3Ascholar.google.com%2F%26output%3Dcite%26scirp%3D"+p+"%26hl%3Dko"
            result = requests.get(bib_url, headers=header)
            soup = bs4.BeautifulSoup(result.content, 'html.parser')
            time.sleep(10)

            try :
                journal = soup.select_one("#gs_citt > table > tbody > tr:nth-child(1) > td > div > i").text
            except :
                journal = ""

            try :
                _apa = soup.select_one("#gs_citt > table > tbody > tr:nth-child(1) > td > div").text
                author = process_apa(_apa)
            except :
                author = ""

            print("[CRAWLED] %s     %s      %s\n" % (paper_name, author, journal))
            f.write("%s+%s+%s\n" % (paper_name, author, journal))
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
    email = "mkang@snu.ac.kr"
    path = "output/{}_{}.csv".format("snu", "강명주")
    crawl(email, path)