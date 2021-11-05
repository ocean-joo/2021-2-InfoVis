from selenium import webdriver
import argparse
import time

title_list = [
    'ENHANCED EXEMPLAR BASED INPAINTING USING PATCH RATIO',
    'IMAGE RESTORATION UNDER CAUCHY NOISE WITH SPARSE REPRESENTATION PRIOR AND TOTAL GENERALIZED VARIATION',
    'Financial series prediction using Attention LSTM',
    'Curvature-weighted Surface Simplification Algorithm using Vertex-based Geometric Features',
    'Troubled-Cell Indicator based on Mean Value Property for Hybrid WENO schemes',
    'Features detection from industrial noisy 3D CT data for reverse engineering',
    'Simultaneous cartoon and texture image restoration with higher-order regularization'
]

def get_bibtex_from_title(target):
    driver = webdriver.Chrome(executable_path='chromedriver')

    print("[System] Try to find bibtex of " + target)

    ss_path = 'https://www.semanticscholar.org/'
    driver.get(url=ss_path)

    # Wait for loading page
    time.sleep(3)

    # Write title in input
    search_input = driver.find_element_by_class_name("legacy__input")
    search_input.send_keys(target)

    # Click Search button
    search_button = driver.find_element_by_class_name("form-submit__icon-text")
    search_button.click()

    # Wait for response
    time.sleep(5)

    try:
        elements_list = driver.find_elements_by_class_name("cl-paper-row")
    except:
        # No result
        driver.close()
        return ""

    # Maybe we don't need to check length of 0?
    if len(elements_list) == 0:
        driver.close()
        return ""

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
        return ""

    # Click cite button (# of buttons are 3 or 4)
    cite_button = first_element\
                .find_elements_by_class_name("cl-paper-action__button")[-1]
    cite_button.click()

    # Wait for response
    time.sleep(2)

    # get bibtex
    bibtex = driver.find_element_by_class_name("formatted-citation--style-bibtex").text

    driver.close()

    return bibtex

if __name__ == '__main__' :
    bibtex_dict = {}

    for title in title_list:
        bibtex = get_bibtex_from_title(title)

        # Not found
        if bibtex == "":
            continue

        bibtex_dict[title] = bibtex
    
    print(bibtex_dict)