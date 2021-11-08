import csv
import os
import json

conf_list = []
lab_list = {}
adj_matrix = []
school_list = ["snu", "kaist", "postech", "yonsei", "korea"]

if __name__ == '__main__' :
    conf_idx = 0
            
    with open('output/conf_csv/conf_with_metadata.csv', 'rt', encoding='utf-8') as input_f:
        rdr = csv.reader(input_f, delimiter='+')

        # Remove first line
        next(rdr)
        for row in rdr:
            new_conf = {"id" : str(conf_idx), "name" : row[0], "impact_score" : float(row[2])}
            conf_list.append(new_conf)
            conf_idx += 1
    
    with open('output/conf_csv/journal_with_metadata.csv', 'rt', encoding='utf-8') as input_f:
        rdr = csv.reader(input_f, delimiter='+')

        # Remove first line
        next(rdr)
        for row in rdr:
            conf_list.append({"id" : str(conf_idx), "name" : row[0], "impact_score" : float(row[1])})
            conf_idx += 1

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
                conf_in_paper = row[2]
                for conf_dict in conf_list:
                    if conf_in_paper in conf_dict["name"] or conf_dict["name"] in conf_in_paper:
                        conf_num_list[int(conf_dict["id"])] += 1
                        total_paper_num += 1

            school_name = bibtex_file.split('_')[0]
            prof_name = bibtex_file.split('_')[-1].split('.')[0]
            lab_list[prof_name] = {"conf_num_list" : conf_num_list, "total_paper_num" : total_paper_num, "school_name" : school_name}
    
    for lab_a in lab_list:
        lab_a_adj = [{"value" : 0, "common_conf" : {}} for _ in range(len(lab_list))]
        for (lab_b_idx, lab_b) in enumerate(lab_list):
            for conf_idx in range(len(conf_list)):
                if lab_list[lab_a]["conf_num_list"][conf_idx] > 0 and lab_list[lab_b]["conf_num_list"][conf_idx] > 0:
                    lab_a_ratio = lab_list[lab_a]["conf_num_list"][conf_idx] / lab_list[lab_a]["total_paper_num"]
                    lab_b_ratio = lab_list[lab_b]["conf_num_list"][conf_idx] / lab_list[lab_b]["total_paper_num"]
                    lab_a_adj[lab_b_idx]["value"] += lab_a_ratio * lab_b_ratio
                    lab_a_adj[lab_b_idx]["common_conf"][conf_idx] = [lab_list[lab_a]["conf_num_list"][conf_idx], lab_list[lab_b]["conf_num_list"][conf_idx]]
        
        adj_matrix.append(lab_a_adj)

    ### json encoding
    lab_json_list = []
    link_list = []

    for (lab_idx, prof_name) in enumerate(lab_list):
        new_node = {}
        new_node["id"] = str(lab_idx)
        new_node["name"] = prof_name
        new_node["scale"] = lab_list[prof_name]["total_paper_num"]
        new_node["cluster"] = school_list.index(lab_list[prof_name]["school_name"])
        lab_json_list.append(new_node)

        for (a_b_adj_idx, a_b_adj) in enumerate(adj_matrix[lab_idx]):
            if a_b_adj_idx >= lab_idx:
                continue
            if a_b_adj["value"] > 0.01:
                new_link = {}
                new_link["id"] = str(lab_idx) + "-" + str(a_b_adj_idx)
                new_link["source"] = lab_idx
                new_link["target"] = a_b_adj_idx
                # TODO : scale weight
                new_link["weight"] = round(a_b_adj["value"] * 100, 2)

                common_conf = []

                for conf_idx in a_b_adj["common_conf"]:
                    common_conf.append({"conf_id" : conf_idx, "source_num" : a_b_adj["common_conf"][conf_idx][0], "target_num" : a_b_adj["common_conf"][conf_idx][1]})
                
                new_link["common_conf"] = common_conf
                
                link_list.append(new_link)

    with open('output/json/lab.json', 'w', encoding='utf-8') as lab_json_file:
        json.dump(lab_json_list, lab_json_file, ensure_ascii=False)

    with open('output/json/link.json', 'w', encoding='utf-8') as link_json_file:
        json.dump(link_list, link_json_file, ensure_ascii=False)

    with open('output/json/conf.json', 'w', encoding='utf-8') as conf_json_file:
        json.dump(conf_list, conf_json_file, ensure_ascii=False)