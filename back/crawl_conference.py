from selenium import webdriver
import argparse

url_list = [
    'https://research.com/conference-rankings/computer-science/2021/computer-vision/page/1',
    'https://research.com/conference-rankings/computer-science/2021/computer-vision/page/2',
    'https://research.com/conference-rankings/computer-science/2021/machine-learning/page/1',
    'https://research.com/conference-rankings/computer-science/2021/machine-learning/page/2',
    'https://research.com/conference-rankings/computer-science/2021/machine-learning/page/3',
    'https://research.com/conference-rankings/computer-science/2021/computational-linguistics-speech-processing/page/1'
]

output_list = {
                'metadata': "output/conf_with_metadata.csv",
                'only_name': "output/conf_name.csv"
            }

conf_dict = {}

def crawl(path, mode):
    driver = webdriver.Chrome(executable_path='chromedriver')
    driver.get(url=path)

    conf_item_list = driver.find_elements_by_class_name("conference-item")
    for conf_item in conf_item_list:
        conf_a_element = conf_item.find_element_by_css_selector("h4 > a")

        if conf_a_element.text not in conf_dict:
            conference_metadata = {}

            print("[System] " + conf_a_element.text + " Crawling Start")

            if mode == 'only_name':
                conf_dict[conf_a_element.text] = conference_metadata
                continue

            ranking_info = conf_item.find_element_by_class_name("rankings-info")
            h5_impact = ranking_info.find_elements_by_css_selector("span > span")
            conference_metadata['h5_index'] = h5_impact[0].text
            conference_metadata['impact_score'] = h5_impact[2].text

            # get more metadata of conference in detail page
            sub_driver = webdriver.Chrome(executable_path='chromedriver')
            item_url = conf_a_element.get_attribute('href')
            sub_driver.get(url=item_url)

            # Check 500 error
            try:
                sub_driver.find_element_by_class_name("conference-details")
            except:
                print("[System] Server may down, crawl next instance")
                continue

            conference_details_elements = sub_driver.find_element_by_class_name("conference-details").find_elements_by_css_selector("p")

            conference_metadata['place'] = conference_details_elements[0].text
            conference_metadata['date'] = conference_details_elements[2].text.split(': ')[1]
            conference_metadata['submission_deadline'] = conference_details_elements[1].text.split(': ')[1]

            conference_metadata['website'] = sub_driver.find_element_by_class_name("text-right").\
                                                find_element_by_css_selector("a").get_attribute('href')

            conference_table_element = sub_driver.find_elements_by_class_name("conference-table")
            conference_metadata['research_ranking'] = conference_table_element[1].find_elements_by_css_selector("div > span")[3].text
            conference_metadata['published_by_top_scientist'] = conference_table_element[1].find_elements_by_css_selector("div > span")[1].text
            conference_metadata['contributing_top_scientist'] = conference_table_element[0].find_elements_by_css_selector("div > span")[3].text

            conf_dict[conf_a_element.text] = conference_metadata

            sub_driver.close()

            print("[System] " + conf_a_element.text + " Crawling End")

    driver.close()

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='Conference Crawler Argparser')
    parser.add_argument('--mode', required=True, type=str, help='mode (only_name / metadata)')

    args = parser.parse_args()

    if args.mode not in ['only_name', 'metadata']:
        print('Should select correct mode')
        exit(1)

    CRAWL = args.mode

    for url in url_list:
        crawl(url, CRAWL)

    with open(output_list[CRAWL], 'w', -1, "utf-8") as f:
        if CRAWL == 'only_name':
            for conf_name, metadata in sorted(conf_dict.items()):
                f.write("%s\n" % conf_name)
        else:
            f.write("%s+%s+%s+%s+%s+%s+%s+%s+%s+%s\n" %
                ("Name","H5_index","impact_score","place",
                "date","submission_deadline","website","research_ranking",
                "published_by_top_scientist","contributing_top_scientist"))
            for conf_name, metadata in sorted(conf_dict.items()):
                f.write("%s+%s+%s+%s+%s+%s+%s+%s+%s+%s\n" % (conf_name,
                    metadata['h5_index'], metadata['impact_score'], metadata['place'],
                    metadata['date'], metadata['submission_deadline'], metadata['website'],
                    metadata['research_ranking'], metadata['published_by_top_scientist'], metadata['contributing_top_scientist']))