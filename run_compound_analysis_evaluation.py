import sys
import os

import devtrans

from evaluate import run_all

script, in_dir = sys.argv


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
        
        relation = entry[7]
        
        samAsa_representation = entry[11] if len(entry) >= 12 else ""
        
        if "-" in word:
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
            if "द्वि" in morph:
                verb = "स्तः"
            elif "बहु" in morph:
                verb = "सन्ति"
            else:
                verb = "अस्ति"
            
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

overall_result, errors = run_all(test_compounds[:], "Unicode")

print("Result: " + str(overall_result))
print(f"Errors in {str(len(errors))} examples")
for id_, cpd, gold_analysis in errors:
    print(id_, cpd)
    for index, word, rel in gold_analysis:
        print(index, word, rel)

