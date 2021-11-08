import csv
import os
import json

conf_list = []
lab_list = {}
adj_matrix = []
school_list = ["snu", "kaist", "postech", "yonsei", "korea"]

if __name__ == '__main__' :

    for conf_file in os.listdir('output/conf_csv'):
        if len(conf_file.split('.')) == 1 or conf_file.split('.')[1] != "csv":
            continue
            
        with open('output/conf_csv/' + conf_file, 'rt', encoding='utf-8') as input_f:
            rdr = csv.reader(input_f, delimiter='+')

            # Remove first line
            next(rdr)
            for row in rdr:
                conf_list.append(row[0])

    for bibtex_file in os.listdir('output/bibtex_csv'):
        if len(bibtex_file.split('.')) == 1 or bibtex_file.split('.')[1] != "csv":
            continue

        with open('output/bibtex_csv/' + bibtex_file, 'rt', encoding='utf-16') as input_f:
            conf_num_list = [0 for _ in range(len(conf_list))]
            total_paper_num = 0

            rdr = csv.reader(input_f, delimiter='+')

            # Remove first line
            next(rdr)
            for row in rdr:
                total_paper_num += 1
                conf_in_paper = row[2]
                for (idx, conf) in enumerate(conf_list):
                    if conf_in_paper in conf or conf in conf_in_paper:
                        conf_num_list[idx] += 1

            school_name = bibtex_file.split('_')[0]
            prof_name = bibtex_file.split('_')[-1].split('.')[0]
            lab_list[prof_name] = {"conf_num_list" : conf_num_list, "total_paper_num" : total_paper_num, "school_name" : school_name}
    
    for lab_a in lab_list:
        lab_a_adj = [0 for _ in range(len(lab_list))]
        for (lab_b_idx, lab_b) in enumerate(lab_list):
            for conf_idx in range(len(conf_list)):
                if lab_list[lab_a]["conf_num_list"][conf_idx] > 0 and lab_list[lab_b]["conf_num_list"][conf_idx] > 0:
                    lab_a_ratio = lab_list[lab_a]["conf_num_list"][conf_idx] / lab_list[lab_a]["total_paper_num"]
                    lab_b_ratio = lab_list[lab_b]["conf_num_list"][conf_idx] / lab_list[lab_b]["total_paper_num"]
                    lab_a_adj[lab_b_idx] += lab_a_ratio * lab_b_ratio
        
        adj_matrix.append(lab_a_adj)

    ### json encoding
    json_dict = {}
    nodes_list = []
    links_list = []

    for (lab_idx, prof_name) in enumerate(lab_list):
        new_node = {}
        new_node["id"] = str(lab_idx)
        new_node["name"] = prof_name
        new_node["scale"] = lab_list[prof_name]["total_paper_num"]
        new_node["cluster"] = school_list.index(lab_list[prof_name]["school_name"])
        nodes_list.append(new_node)

        for (a_b_adj_idx, a_b_adj) in enumerate(adj_matrix[lab_idx]):
            if a_b_adj_idx >= lab_idx:
                continue
            if a_b_adj > 0:
                new_link = {}
                new_link["id"] = str(lab_idx) + "-" + str(a_b_adj_idx)
                new_link["source"] = lab_idx
                new_link["target"] = a_b_adj_idx
                # TODO : scale weight
                new_link["weight"] = a_b_adj * 100
                links_list.append(new_link)
    
    json_dict["nodes"] = nodes_list
    json_dict["links"] = links_list

    with open('output/json/weight.json', 'w') as json_file:
        json.dump(json_dict, json_file)