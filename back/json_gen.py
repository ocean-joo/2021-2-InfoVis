import csv
import os
import json

# parameter
W_THR = 0.01

# will be dumped into json
conf_list = []
raw_lab_list = []
lab_list = []
link_list = []

school_list = ["snu", "kaist", "postech", "yonsei", "korea"]
lab_in_conf_cnt = [] # lab_in_conf_cnt[A][B] : how many paper lab A published on conference B.
adj_matrix = [] # adj_matrix[A][B] : weight, common conference for lab A and lab B

if __name__ == '__main__' :
    lab_id_idx = 0
    conf_id_idx = 0
            
    with open('output/conf_csv/conf_with_metadata.csv', 'rt', encoding='utf-8') as input_f:
        rdr = csv.reader(input_f, delimiter='+')

        # Remove first line
        next(rdr)
        for row in rdr:
            new_conf = {"id" : str(conf_id_idx), "name" : row[0], "impact_score" : float(row[2])}
            conf_list.append(new_conf)
            conf_id_idx += 1

    with open('output/conf_csv/journal_with_metadata.csv', 'rt', encoding='utf-8') as input_f:
        rdr = csv.reader(input_f, delimiter='+')

        # Remove first line
        next(rdr)
        for row in rdr:
            conf_list.append({"id" : str(conf_id_idx), "name" : row[0], "impact_score" : float(row[1])})
            conf_id_idx += 1

    for school in school_list:
        lab_info_file = 'output/lab_csv/{}_homepage.csv'.format(school)

        with open(lab_info_file, 'rt', encoding='cp949') as input_f:
            rdr = csv.reader(input_f, delimiter=',')
            for row in rdr:
                lab_el = {}
                lab_el["prof_name"] = row[0]
                lab_el["email"] = row[1]
                lab_el["href"] = row[2]
                lab_el["name"] = row[3]
                lab_el["description"] = row[4]
                lab_el["school"] = school

                raw_lab_list.append(lab_el)

    # Filter lab which does not have paper in google scholar
    for lab in raw_lab_list:
        bibtex_file = 'output/bibtex_csv/{}_bibtex_{}.csv'.format(lab["school"], lab["prof_name"])

        if not os.path.exists(bibtex_file):
            continue
        
        with open(bibtex_file, 'rt', encoding='utf-16') as input_f:
            if len(input_f.readlines()) == 1:
                continue
        
        lab_el = {}
        lab_el["id"] = lab_id_idx
        lab_el["prof_name"] = lab["prof_name"]
        lab_el["email"] = lab["email"]
        lab_el["href"] = lab["href"]
        lab_el["name"] = lab["name"]
        lab_el["school"] = lab["school"]
        lab_el["description"] = lab["description"]

        lab_list.append(lab_el)
        lab_id_idx += 1
    
    for lab in lab_list:
        bibtex_file = 'output/bibtex_csv/{}_bibtex_{}.csv'.format(lab["school"], lab["prof_name"])
        with open(bibtex_file, 'rt', encoding='utf-16') as input_f:
            conf_num_list = [0 for _ in range(len(conf_list))]
            paper_list = []

            rdr = csv.reader(input_f, delimiter='+')
            # Remove first line
            next(rdr)

            # TODO : should separate top 1000 conf and total paper
            for row in rdr:
                conf_in_paper = row[2]
                for conf_id, conf_dict in enumerate(conf_list):
                    if conf_in_paper in conf_dict["name"] or conf_dict["name"] in conf_in_paper:
                        paper_list.append({"title" : row[0], "conf_id" : conf_id, "href" : row[3], "year" : row[4], "apa" : row[5]})
                        conf_num_list[conf_id] += 1

            lab["total_paper_num"] = len(paper_list)
            lab["paper"] = paper_list

            lab_in_conf_cnt.append(conf_num_list)

    for (a_id, lab_a) in enumerate(lab_list):
        lab_a_adj = [{"value" : 0, "common_conf" : {}} for _ in range(len(lab_list))]
        for (b_id, lab_b) in enumerate(lab_list):
            for (conf_id, conf) in enumerate(conf_list):
                if lab_in_conf_cnt[a_id][conf_id] > 0 and lab_in_conf_cnt[b_id][conf_id] > 0:
                    lab_a_ratio = lab_in_conf_cnt[a_id][conf_id] / lab_a["total_paper_num"]
                    lab_b_ratio = lab_in_conf_cnt[b_id][conf_id] / lab_b["total_paper_num"]
                    lab_a_adj[b_id]["value"] += lab_a_ratio * lab_b_ratio
                    lab_a_adj[b_id]["common_conf"][conf_id] = [lab_in_conf_cnt[a_id][conf_id], lab_in_conf_cnt[b_id][conf_id]]
        
        adj_matrix.append(lab_a_adj)

    ### json encoding
    for (a_id, lab_a) in enumerate(lab_list):
        for (b_id, lab_b) in enumerate(lab_list):
            if a_id >= b_id:
                continue
            
            if adj_matrix[a_id][b_id]["value"] > W_THR:
                new_link = {}
                new_link["id"] = str(a_id) + "-" + str(b_id)
                new_link["source"] = a_id
                new_link["target"] = b_id
                # TODO : scale weight
                new_link["weight"] = round(adj_matrix[a_id][b_id]["value"] * 100, 2)

                common_conf = []

                for conf_idx in adj_matrix[a_id][b_id]["common_conf"]:
                    common_conf.append({"conf_id" : conf_idx, "source_num" : adj_matrix[a_id][b_id]["common_conf"][conf_idx][0], "target_num" : adj_matrix[a_id][b_id]["common_conf"][conf_idx][1]})
                
                new_link["common_conf"] = common_conf
                
                link_list.append(new_link)

    with open('output/json/lab.json', 'w', encoding='utf-8') as lab_json_file:
        json.dump(lab_list, lab_json_file, ensure_ascii=False)

    with open('output/json/link.json', 'w', encoding='utf-8') as link_json_file:
        json.dump(link_list, link_json_file, ensure_ascii=False)

    with open('output/json/conf.json', 'w', encoding='utf-8') as conf_json_file:
        json.dump(conf_list, conf_json_file, ensure_ascii=False)