from selenium import webdriver
import argparse

url_list = [
    'https://research.com/journals-rankings/computer-science/2021/machine-learning/page/1',
    'https://research.com/journals-rankings/computer-science/2021/machine-learning/page/2',
    'https://research.com/journals-rankings/computer-science/2021/computer-vision/page/1',
    'https://research.com/journals-rankings/computer-science/2021/computational-linguistics-speech-processing/page/1'
]

output_list = {
                'metadata': "output/journal_with_metadata.csv",
                'only_name': "output/journal_name.csv"
            }

jn_dict = {}

def crawl(path, mode):
    driver = webdriver.Chrome(executable_path='chromedriver')
    driver.get(url=path)

    jn_item_list = driver.find_elements_by_class_name("journal-item")
    for jn_item in jn_item_list:
        jn_a_element = jn_item.find_element_by_css_selector("h4 > a")

        if jn_a_element.text not in jn_dict:
            jn_metadata = {}

            print("[System] " + jn_a_element.text + " Crawling Start")

            if mode == 'only_name':
                jn_dict[jn_a_element.text] = jn_metadata
                continue

            # get metadata in detail page
            sub_driver = webdriver.Chrome(executable_path='chromedriver')
            item_url = jn_a_element.get_attribute('href')
            sub_driver.get(url=item_url)

            # Check 500 error
            try:
                sub_driver.find_element_by_class_name("first-section")
            except:
                print("[System] Server may down, crawl next instance")
                continue

            jn_ranking_metrics = sub_driver.find_elements_by_class_name("conference-table")

            jn_metadata['impact_score'] = jn_ranking_metrics[0].find_elements_by_css_selector("span")[1].text
            jn_metadata['jcr_impact_factor'] = jn_ranking_metrics[0].find_elements_by_css_selector("span")[3].text
            jn_metadata['scimago_sjr'] = jn_ranking_metrics[0].find_elements_by_css_selector("span")[5].text
            jn_metadata['scopus_citescore'] = jn_ranking_metrics[0].find_elements_by_css_selector("span")[7].text

            jn_metadata['scimago_h_index'] = jn_ranking_metrics[1].find_elements_by_css_selector("span")[1].text
            jn_metadata['research_ranking'] = jn_ranking_metrics[1].find_elements_by_css_selector("span")[4].text
            jn_metadata['number_of_top_scientist'] = jn_ranking_metrics[1].find_elements_by_css_selector("span")[6].text
            jn_metadata['documents_by_top_scientist'] = jn_ranking_metrics[1].find_elements_by_css_selector("span")[8].text

            jn_metadata['issn'] = jn_ranking_metrics[2].find_elements_by_css_selector("span")[1].text
            jn_metadata['publisher'] = jn_ranking_metrics[2].find_element_by_css_selector("img").get_attribute("alt")
            jn_metadata['periodicity'] = jn_ranking_metrics[2].find_elements_by_css_selector("span")[5].text
            jn_metadata['editor_in_chief'] = jn_ranking_metrics[2].find_elements_by_css_selector("span")[7].text
            jn_metadata['website'] = jn_ranking_metrics[2].find_elements_by_css_selector("span")[9].text

            jn_dict[jn_a_element.text] = jn_metadata

            sub_driver.close()

            print("[System] " + jn_a_element.text + " Crawling End")

            break

    driver.close()

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='Journal Crawler Argparser')
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
            for jn_name, metadata in sorted(jn_dict.items()):
                f.write("%s\n" % jn_name)
        else:
            f.write("Name,impact_score,jcr_impact_factor,scimago_sjr,\
                    scopus_citescore,scimago_h_index,research_ranking,\
                    number_of_top_scientist,documents_by_top_scientist,\
                    issn,publisher,periodicity,editor_in_chief,website\n")

            for jn_name, metadata in sorted(jn_dict.items()):
                f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (jn_name,
                    metadata['h5_index'], metadata['impact_score'], metadata['jcr_impact_factor'],
                    metadata['scimago_sjr'], metadata['scopus_citescore'], metadata['scimago_h_index'],
                    metadata['research_ranking'], metadata['number_of_top_scientist'], metadata['documents_by_top_scientist'],
                    metadata['publisher'], metadata['periodicity'], metadata['editor_in_chief'], metadata['website']))