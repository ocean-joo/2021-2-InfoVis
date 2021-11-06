from selenium import webdriver
import time
import csv
import os
import warnings

def get_bibtex_and_APA_from_title(target):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-logging') 
    driver = webdriver.Chrome(executable_path='chromedriver', options=options)

    print("[System] Try to find bibtex of " + target)

    ss_path = 'https://www.semanticscholar.org/'
    driver.get(url=ss_path)

    # Wait for loading page
    time.sleep(2)

    # Write title in input
    search_input = driver.find_element_by_class_name("legacy__input")
    search_input.send_keys(target)

    # Click Search button
    search_button = driver.find_element_by_class_name("form-submit__icon-text")
    search_button.click()

    # Wait for response
    time.sleep(3)

    try:
        elements_list = driver.find_elements_by_class_name("cl-paper-row")
    except:
        # No result
        driver.close()
        return "", ""

    # Maybe we don't need to check length of 0?
    if len(elements_list) == 0:
        driver.close()
        return "", ""

    # Check only first searched element
    first_element = elements_list[0]

    title_char_list = first_element\
                .find_element_by_css_selector("a > div > span")\
                .find_elements_by_css_selector("*")

    title = ""

    # Title split into multiple elements.
    # We should merge them in one string
    for title_char_el in title_char_list:
        title += title_char_el.text

    # If first title is different from target, continue
    if title.lower() != target.lower().replace(" ", ""):
        driver.close()
        return "", ""

    # Click cite button (# of buttons are 3 or 4)
    try:
        cite_button = first_element\
                    .find_elements_by_class_name("cl-paper-action__button")[-1]
        cite_button.click()
    except:
        driver.close()
        return "", ""

    # Wait for response
    time.sleep(2)

    # get bibtex
    bibtex = driver.find_element_by_class_name("formatted-citation--style-bibtex").text

    # Click APA button
    try:
        apa_button = driver.find_elements_by_class_name("cite-modal__button")[2]
        apa_button.click()
    except:
        driver.close()
        return "", ""

    # Wait for response
    time.sleep(2)

    apa = driver.find_element_by_class_name("formatted-citation--style-apa").text

    driver.close()

    return bibtex, apa

if __name__ == '__main__' :
    warnings.filterwarnings('ignore')

    for title_file_name in os.listdir('data'):
        input_path = 'data/' + title_file_name
        output_path = 'output/bibtex_' + title_file_name

        input_f = open(input_path, 'rt', encoding='utf-16')
        rdr = csv.reader(input_f, delimiter='+')

        res_f = open(output_path, 'w', encoding='utf-16')
        wr = csv.writer(res_f, delimiter='+', newline='')
        wr.writerow(['title', 'author', 'conf_name', 'href', 'year', 'apa'])

        for row in rdr:
            title = row[0]
            if len(title.split('] ')) > 1:
                title = title.split('] ')[1]
            
            bibtex, apa = get_bibtex_and_APA_from_title(title)

            # Not found
            if bibtex == "":
                continue

            bib_dict = {"title" : title, "href" : row[1], "apa" : apa}

            for bibrow in bibtex.split("\n"):
                if "author" in bibrow:
                    bib_dict['author'] = bibrow.split('{')[1].split('}')[0]
                elif "journal" in bibrow:
                    bib_dict['conf_name'] = bibrow.split('{')[1].split('}')[0]
                elif "year" in bibrow:
                    bib_dict['year'] = bibrow.split('{')[1].split('}')[0]

            # if not journal, continue
            if "journal" not in bib_dict:
                continue

            wr.writerow([bib_dict['title'], bib_dict['author'], bib_dict['conf_name'],
                bib_dict['href'], bib_dict['year'], bib_dict['apa']])

        input_f.close()
        res_f.close()