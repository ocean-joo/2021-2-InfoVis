from selenium import webdriver
import time

CRAWL = 'conf' # vision, ml

url_list = [
    'https://research.com/conference-rankings/computer-science/2021/computer-vision/page/1',
    'https://research.com/conference-rankings/computer-science/2021/computer-vision/page/2',
    'https://research.com/conference-rankings/computer-science/2021/machine-learning/page/1',
    'https://research.com/conference-rankings/computer-science/2021/machine-learning/page/2',
    'https://research.com/conference-rankings/computer-science/2021/machine-learning/page/3'
]

output_list = {
                'conf': "output/conference.csv"
            }

conf_list = []

def crawl(path):
    driver = webdriver.Chrome(executable_path='chromedriver')
    driver.get(url=path)

    conf_item_list = driver.find_elements_by_class_name("conference-item")
    for conf_item in conf_item_list:
        name = conf_item.find_element_by_css_selector("h4 > a").text

        if name not in conf_list:
            conf_list.append(name)

    driver.close()

if __name__ == '__main__' :
    for url in url_list:
        crawl(url)

    conf_list.sort()

    with open('output/conf.csv', 'w') as f:
        for conf_name in conf_list:
            f.write("%s\n" % (conf_name))