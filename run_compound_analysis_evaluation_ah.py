import sys
import os

import json

import devtrans as dt

from evaluate import run_all

script, inp_, out_, err, res, pair = sys.argv


rel_codes = {
    "Tn" : "नञ्-तत्पुरुषः",
    "T1" : "प्रथमा-तत्पुरुषः",
    "T2" : "द्वितीया-तत्पुरुषः",
    "T3" : "तृतीया-तत्पुरुषः",
    "T4" : "चतुर्थी-तत्पुरुषः",
    "T5" : "पञ्चमी-तत्पुरुषः",
    "T6" : "षष्ठी-तत्पुरुषः",
    "T7" : "सप्तमी-तत्पुरुषः",
    "T" : "तत्पुरुषः",
    "Td" : "द्विगु-तत्पुरुषः",
    "Tu" : "उपपद-तत्पुरुषः",
    "Tp" : "प्रादि-तत्पुरुषः",
    "Tg" : "गति-तत्पुरुषः",
    "K" : "कर्मधारयः",
    "K1" : "कर्मधारयः_1",
    "K2" : "कर्मधारयः_2",
    "K3" : "कर्मधारयः_3",
    "K4" : "कर्मधारयः_4",
    "K5" : "कर्मधारयः_5",
    # "K6" : "कर्मधारयः_6",
    "K7" : "कर्मधारयः", # Check if it is applicable
    "Km" : "कर्मधारयः", # "मध्यमपदलोपि-कर्मधारयः"
    "Bvs" : "बहुव्रीहिः",
    "A" : "अव्ययीभावः",
    "A1" : "अव्ययीभावः_1",
    "A2" : "अव्ययीभावः_2",
    "A3" : "अव्ययीभावः_3",
    "A4" : "अव्ययीभावः_4",
    "A5" : "अव्ययीभावः_5",
    "A6" : "अव्ययीभावः_6",
    "A7" : "अव्ययीभावः_7",
    "D" : "द्वन्द्वः",
    "Di" : "इतरेतर-द्वन्द्वः",
    "Di" : "समाहार-द्वन्द्वः",
    "U" : "उपपद-तत्पुरुषः",
    "B" : "बहुव्रीहिः",
    "Bs" : "बहुव्रीहिः", # "समानाधिकरण-बहुव्रीहिः"
    "Bs2" : "बहुव्रीहिः_2", # "द्वितीयार्थ-बहुव्रीहिः"
    "Bs3" : "बहुव्रीहिः_3", # "तृतीयार्थ-बहुव्रीहिः"
    "Bs4" : "बहुव्रीहिः_4", # "चतुर्थ्यर्थ-बहुव्रीहिः"
    "Bs5" : "बहुव्रीहिः_5", # "पञ्चम्यर्थ-बहुव्रीहिः"
    "Bs6" : "बहुव्रीहिः_6", # "षष्ठ्यर्थ-बहुव्रीहिः"
    "Bs7" : "बहुव्रीहिः_7", # "सप्तम्यर्थ-बहुव्रीहिः"
    "Bsmn" : "नञ्-बहुव्रीहिः",
    "BvS" : "बहुव्रीहिः", # "सहपूर्वपद-व्यधिकरण-बहुव्रीहिः"
    "S" : "केवल-समासः",
}

def rel_for_type(rel_type):
    """ """

    return rel_codes.get(rel_type, rel_type)


def read_contents(name_):
    """ """
    
    file_ = open(name_, "r", encoding="utf-8")
    file_contents = file_.read()
    file_.close()
    
    file_lines = list(filter(None, file_contents.split("\n")))
    
    return file_lines[:]
    

def extract_compounds(lines):
    """Extracts compound type and compound word from the input."""
    
    compounds = []
    cpd_items = []
    cpd_id = 0

    cur_compound = ""
    cur_cmpnt_index = 0
    cur_compound_start_index = 0
    cur_sent_index = 1

    error = False
    
    for line in lines:
        parts = line.split("\t")
        
        index = parts[0].strip()
        word = parts[1].strip()
        no_of_components = parts[2].strip()
        rel_index = parts[4].strip()
        rel_type = parts[5].strip()

        if not word:
            cur_sent_index += 1
            continue

        if word == "DUMMY" or rel_type == "No_rel" or "(" in word or ")" in word:
            continue
        
        if "-" in word:
            rel_type = rel_for_type(rel_type)
            cur_cmpnt_index += 1
            if not cur_compound:
                cur_compound_start_index = int(index)
            component_index = f"1.{cur_cmpnt_index}"
            rel_component_index = f"1.{int(rel_index) - cur_compound_start_index + 1}"
            rel = f"{rel_type},{rel_component_index}"
            cur_compound += word
            cpd_items.append((component_index, word, rel, ""))
        elif rel_type == "Comp_root":
            if not cur_compound:
                print(f"Warning: Compound root found without preceding compound: {word} at index {cur_sent_index}.{index}")
                cpd_items = []
                cur_compound = ""
                continue
            cur_cmpnt_index += 1
            component_index = f"1.{cur_cmpnt_index}"
            cpd_items.append((component_index, word, "-,-", ""))
            # Instead of providing a verb, we provide a dummy entry
            # to indicate the end of the compound.
            cpd_items.append((f"2.1", ".", "-,-", ""))
            cur_compound += word
            cpd_id += 1
            compounds.append((f"{cpd_id}", cur_compound, cpd_items))
            cpd_items = []
            cur_compound = ""
            cur_cmpnt_index = 0
            cur_compound_start_index = 0
        
    return compounds, error


lines = read_contents(inp_)
compounds, error = extract_compounds(lines)

if error:
    print("Error in input file format. Please check the input file.")
    sys.exit(1)

test_compounds = []

for id_, cpd_str, cpd_details in compounds:
    new_cpd_details = [ x[:-1] for x in cpd_details ]
    
    test_compounds.append((id_, cpd_str, new_cpd_details))

print(test_compounds)

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




