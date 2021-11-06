import bs4, time
import requests
from requests.auth import HTTPProxyAuth
import random
import argparse

def crawl(email, output) :
    header =  {'User-Agent': 'Mozilla/5.0'}
    url = "https://scholar.google.co.kr/scholar?q=" + email

    result = requests.get(url, headers=header)
    soup = bs4.BeautifulSoup(result.content, 'html.parser')

    f = open(output, 'w',encoding='UTF-16')
    
    try :
        paper_num_str = soup.select_one("#gs_ab_md > div").text
    except :
        print(soup.contents)
        exit()

    try :
        paper_num = int("".join([c for c in paper_num_str.split("(")[0] if c.isdigit()]))
        print("[*] %s -> %d" % (email, paper_num))
    except :
        print("[*] No Paper for %s\n" % email)
        return

    time.sleep(random.randint(3, 8))

    for i in range(0, int((paper_num)/10)+1) :
        if i == 0 :
            sub_url = url
        else :
            sub_url = url + "&start=" + str(i*10)

        sub_result = requests.get(sub_url, headers=header)
        sub_soup = bs4.BeautifulSoup(sub_result.content, 'html.parser')

        time.sleep(random.randint(3, 8))

        if len(sub_soup.select("#gs_res_ccl_mid > div")) == 0 :
            print("MAYBE BANNED")

        for paper_content in sub_soup.select("#gs_res_ccl_mid > div") :
            try :
                paper_name = paper_content.select_one("h3").text
                # if paper_name.lower().startswith("[pdf]") :
                #     paper_name = paper_name[6:]
                link = paper_content.select_one("h3 > a").get("href")
            except :
                print("[FAILED] %s\n" % paper_name)

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

    parser = argparse.ArgumentParser(description='Conference Crawler Argparser')
    parser.add_argument('--school', '-s', required=True, type=str, help='school')
    parser.add_argument('--banned', '-b', type=int, default=0, help='banned point')
    args = parser.parse_args()

    if args.school not in meta_path_dict:
        exit(1)

    meta = meta_path_dict[args.school]
    
    with open(meta, 'r') as f :

        lines = f.readlines()
        for i, line in enumerate(lines) :
            # Start crawling from banned point
            if i < args.banned :
                continue
            name, email, _ = line.split(",")
            path = "output/{}_title_{}.csv".format(args.school, name)

            crawl(email, path) 