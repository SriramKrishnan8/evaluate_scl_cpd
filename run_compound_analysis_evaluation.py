import sys
import os

import json

import devtrans

from evaluate import run_all

script, in_dir, out_, err, res, pair = sys.argv


def read_contents(name_):
    """ """
    
    file_ = open(name_, "r", encoding="utf-8")
    file_contents = file_.read()
    file_.close()
    
    file_lines = list(filter(None, file_contents.split("\n")))
    
    return file_lines[:]
    

def get_rel_c_index(relation):
    """ """
    
    rel = relation.split(",")
    
    rel_type = rel[0]
    rel_index = rel[1]
    
    # To make sure indices like 4.1.1 are handled
    rel_index_split = rel_index.split(".")
    rel_w_index = rel_index_split[0]
    rel_c_index = rel_index_split[-1]
    
#    rel_w_index, rel_c_index = rel_index.split(".")
    
    return rel_type, rel_c_index


compounds = []

compound_id = 0

for f in os.listdir(in_dir):
    f_name = os.path.join(in_dir, f)
    
    f_lines = read_contents(f_name)
    
    compound_details = []
    in_cpd = False
    compound_str = ""
    cur_cmpnt_id = 0
    
    for x in f_lines[1:]:
        entry = x.split("\t")
        
        index = entry[0]
        word = entry[1]
        
        morph = entry[5]
        
        relation = entry[6]
        
        samAsa_representation = entry[11] if len(entry) >= 12 else ""
        
        if "-" in word and "(" not in word:
            compound_str += word
            cur_cmpnt_id += 1
            
            index_split = index.split(".")
            w_index = index_split[0]
            c_index = index_split[-1]
            
#            w_index, c_index = index.split(".")
            
            rel_type, rel_c_index = get_rel_c_index(relation)
            
            compound_details.append((f"1.{c_index}", word, f"{rel_type},1.{rel_c_index}", samAsa_representation))
            in_cpd = True
        elif in_cpd:
            compound_str += word
            
            # To make sure indices like 4.1.1 are handled
            index_split = index.split(".")
            w_index = index_split[0]
            c_index = index_split[-1]
            
#            w_index, c_index = index.split(".")
            
            compound_details.append((f"1.{c_index}", word, "कर्ता,2.1", samAsa_representation))
            compound_id += 1
            if any([x in morph for x in ["1", "2"]]):
                if "द्वि" in morph:
                    verb = "स्तः"
                elif "बहु" in morph:
                    verb = "सन्ति"
                else:
                    verb = "अस्ति"
            else:
                if "द्वि" in morph:
                    verb = "भवतः"
                elif "बहु" in morph:
                    verb = "भवन्ति"
                else:
                    verb = "भवति"
            
            compound_details.append(("2.1", verb, f"अभिहित_कर्ता,1.{c_index}", ""))
            
            compounds.append((compound_id, compound_str + " " + verb, compound_details))
            compound_details = []
            in_cpd = False
            compound_str = ""
        else:
            pass
    

test_compounds = []

for id_, cpd_str, cpd_details in compounds:
    new_cpd_details = [ x[:-1] for x in cpd_details ]
    
    test_compounds.append((id_, cpd_str, new_cpd_details))

overall_result, errors, temp_results, gold_pred_pairs = run_all(test_compounds[:], "Unicode")

out_lines = []
for id_, line, gold_analysis, status, pred_analysis, rel_type_score, rel_index_score, complete_rel_score, no_analysis in temp_results:
    out_lines.append("\t".join((str(id_), line, json.dumps(gold_analysis, ensure_ascii=False), status, json.dumps(pred_analysis, ensure_ascii=False), rel_type_score, rel_index_score, complete_rel_score, no_analysis)))

out_f = open(out_, "w", encoding="utf-8")
out_f.write("\n".join(out_lines))
out_f.close()

err_lines = []
for id_, line, gold_analysis in errors:
    err_lines.append("\t".join((str(id_), line, json.dumps(gold_analysis, ensure_ascii=False))))

err_f = open(err, "w", encoding="utf-8")
err_f.write("\n".join(err_lines))
err_f.close()

pair_f = open(pair, "w", encoding="utf-8")
pair_f.write("\n".join(["\t".join(x) for x in gold_pred_pairs]))
pair_f.close()

with open(res, "w", encoding="utf-8") as f:
    f.write(json.dumps(overall_result, ensure_ascii=False))

