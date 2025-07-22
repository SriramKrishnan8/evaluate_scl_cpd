import sys
import os

import json

import devtrans as dt

from evaluate import run_all

script, inp_, out_, err, res = sys.argv


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
    "K" : "कर्मधारयः",
    "K1" : "कर्मधारयः_1",
    "K2" : "कर्मधारयः_2",
    "K3" : "कर्मधारयः_3",
    "K4" : "कर्मधारयः_4",
    "K5" : "कर्मधारयः_5",
    "Bvs" : "बहुव्रीहिः",
    "A1" : "अव्ययीभावः_1",
    "A2" : "अव्ययीभावः_2",
    "A3" : "अव्ययीभावः_3",
    "A4" : "अव्ययीभावः_4",
    "A5" : "अव्ययीभावः_5",
    "A6" : "अव्ययीभावः_6",
    "A7" : "अव्ययीभावः_7",
    "D" : "इतरेत-द्वन्द्वः",
    "U" : "उपपद-तत्पुरुषः",
    "B" : "बहुव्रीहिः",
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
    

compound_items = read_contents(inp_)
compounds = []

for i in range(len(compound_items)):
    cpd_item = compound_items[i]
    cpd_type, cpd_wx = cpd_item.split("\t")

    cpd_items = []

    cpd_id = str(i + 1)
    # cpd = dt.wx2dev(cpd_wx)
    cpd = cpd_wx
    cmpnts = cpd.split("-")
    num_of_cmpnts = len(cmpnts)
    for c in range(len(cmpnts)):
        cmpnt = cmpnts[c]
        cpd_index = "1." + str(c + 1)
        word = cmpnt + "-" if c < num_of_cmpnts - 1 else cmpnt
        rel_type = rel_for_type(cpd_type)
        rel_index = "1." + str(c + 2)
        if c < num_of_cmpnts - 1:
            rel = rel_type + "," + rel_index
        else:
            rel = "कर्ता,2.1"
        
        cpd_items.append((cpd_index, word, rel, ""))
    cpd_items.append(("2.1", "अस्ति", "-,-", ""))

    compounds.append((str(i + 1), cpd + " अस्ति", cpd_items))


test_compounds = []

for id_, cpd_str, cpd_details in compounds:
    new_cpd_details = [ x[:-1] for x in cpd_details ]
    
    test_compounds.append((id_, cpd_str, new_cpd_details))

overall_result, errors, temp_results = run_all(test_compounds[:], "Unicode")

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

with open(res, "w", encoding="utf-8") as f:
    f.write(json.dumps(overall_result, ensure_ascii=False))




