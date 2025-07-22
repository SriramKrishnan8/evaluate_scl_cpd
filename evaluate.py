import os
import sys

import subprocess as sp

import json
import numpy as np

from tqdm import tqdm

import devtrans


cgi_file = "/usr/lib/cgi-bin/scl/MT/anusaaraka.cgi"


fine_to_coarse_dev = {
    "अव्ययीभावः" : "अव्ययीभावः",
    "इतरेतर-द्वन्द्वः" : "द्वन्द्वः",
    "उपपद-तत्पुरुषः" : "तत्पुरुषः",
    "कर्मधारयः" : "तत्पुरुषः",
    "केवल-समासः" : "तत्पुरुषः",
    "चतुर्थी-तत्पुरुषः" : "तत्पुरुषः",
    "तत्पुरुषः" : "तत्पुरुषः",
    "तृतीया-तत्पुरुषः" : "तत्पुरुषः",
    "द्वन्द्वः" : "द्वन्द्वः",
    "द्वितीया-तत्पुरुषः" : "तत्पुरुषः",
    "नञ्-तत्पुरुषः" : "तत्पुरुषः",
    "नञ्-बहुव्रीहिः" : "बहुव्रीहिः",
    "पञ्चमी-तत्पुरुषः" : "तत्पुरुषः",
    "प्रादि-तत्पुरुषः" : "तत्पुरुषः",
    "बहुव्रीहिः" : "बहुव्रीहिः",
    "षष्ठी-तत्पुरुषः" : "तत्पुरुषः",
    "सप्तमी-तत्पुरुषः" : "तत्पुरुषः",
    "उपमानम्" : "तत्पुरुषः",
    "द्विगु-तत्पुरुषः" : "तत्पुरुषः",
    "कर्मधारयः-1" : "कर्मधारयः",
    "कर्मधारयः-2" : "कर्मधारयः",
    "कर्मधारयः-3" : "कर्मधारयः",
    "कर्मधारयः-4" : "कर्मधारयः",
    "कर्मधारयः-5" : "कर्मधारयः",
    "-" : "तत्पुरुषः",
}

cpd_codes = {
    "नञ्_त_पु" : "नञ्-तत्पुरुषः",
    "त_पु_1" : "प्रथमा-तत्पुरुषः",
    "त_पु_2" : "द्वितीया-तत्पुरुषः",
    "त_पु_3" : "तृतीया-तत्पुरुषः",
    "त_पु_4" : "चतुर्थी-तत्पुरुषः",
    "त_पु_5" : "पञ्चमी-तत्पुरुषः",
    "त_पु_6" : "षष्ठी-तत्पुरुषः",
    "त_पु_7" : "सप्तमी-तत्पुरुषः",
    "त_पु" : "तत्पुरुषः",
    "त_पु_द्विगु" : "द्विगु-तत्पुरुषः",
    "उ_प_त_पु" : "उपपद-तत्पुरुषः",
    "क_धा" : "कर्मधारयः",
    "क_धा_1" : "कर्मधारयः_1",
    "क_धा_2" : "कर्मधारयः_2",
    "क_धा_3" : "कर्मधारयः_3",
    "क_धा_4" : "कर्मधारयः_4",
    "क_धा_5" : "कर्मधारयः_5",
    "ब_व्री" : "बहुव्रीहिः",
    "अ_भा_1" : "अव्ययीभावः_1",
    "अ_भा_2" : "अव्ययीभावः_2",
    "अ_भा_3" : "अव्ययीभावः_3",
    "अ_भा_4" : "अव्ययीभावः_4",
    "अ_भा_5" : "अव्ययीभावः_5",
    "अ_भा_6" : "अव्ययीभावः_6",
    "अ_भा_7" : "अव्ययीभावः_7",
    "द्वन्द्वः" : "इतरेतर-द्वन्द्वः",
    "-" : "तत्पुरुषः",
}

cpd_codes_2 = {
    "नञ्_त_पु" : "नञ्-तत्पुरुषः",
    "त_पु_1" : "प्रथमा-तत्पुरुषः",
    "त_पु_2" : "द्वितीया-तत्पुरुषः",
    "त_पु_3" : "तृतीया-तत्पुरुषः",
    "त_पु_4" : "चतुर्थी-तत्पुरुषः",
    "त_पु_5" : "पञ्चमी-तत्पुरुषः",
    "त_पु_6" : "षष्ठी-तत्पुरुषः",
    "त_पु_7" : "सप्तमी-तत्पुरुषः",
    "त_पु" : "तत्पुरुषः",
    "त_पु_द्विगु" : "द्विगु-तत्पुरुषः",
    "उ_प_त_पु" : "उपपद-तत्पुरुषः",
    "क_धा" : "कर्मधारयः",
    "ब_व्री" : "बहुव्रीहिः",
    "अव्ययीभावः" : "अव्ययीभावः",
    "अ_भा_1" : "अव्ययीभावः",
    "अ_भा_2" : "अव्ययीभावः",
    "अ_भा_3" : "अव्ययीभावः",
    "अ_भा_4" : "अव्ययीभावः",
    "अ_भा_5" : "अव्ययीभावः",
    "अ_भा_6" : "अव्ययीभावः",
    "अ_भा_7" : "अव्ययीभावः",
    "क_धा_1" : "कर्मधारयः",
    "क_धा_2" : "कर्मधारयः",
    "क_धा_3" : "कर्मधारयः",
    "क_धा_4" : "कर्मधारयः",
    "क_धा_5" : "कर्मधारयः",
    "द्वन्द्वः" : "द्वन्द्वः",
    "इतरेतर-द्वन्द्वः" : "द्वन्द्वः",
    "अव्ययीभावः_1" : "अव्ययीभावः",
    "अव्ययीभावः_2" : "अव्ययीभावः",
    "अव्ययीभावः_3" : "अव्ययीभावः",
    "अव्ययीभावः_4" : "अव्ययीभावः",
    "अव्ययीभावः_5" : "अव्ययीभावः",
    "अव्ययीभावः_6" : "अव्ययीभावः",
    "अव्ययीभावः_7" : "अव्ययीभावः",
    "कर्मधारयः_1" : "कर्मधारयः",
    "कर्मधारयः_2" : "कर्मधारयः",
    "कर्मधारयः_3" : "कर्मधारयः",
    "कर्मधारयः_4" : "कर्मधारयः",
    "कर्मधारयः_5" : "कर्मधारयः",
    "अव्ययीभावः-1" : "अव्ययीभावः",
    "अव्ययीभावः-2" : "अव्ययीभावः",
    "अव्ययीभावः-3" : "अव्ययीभावः",
    "अव्ययीभावः-4" : "अव्ययीभावः",
    "अव्ययीभावः-5" : "अव्ययीभावः",
    "अव्ययीभावः-6" : "अव्ययीभावः",
    "अव्ययीभावः-7" : "अव्ययीभावः",
    "कर्मधारयः-1" : "कर्मधारयः",
    "कर्मधारयः-2" : "कर्मधारयः",
    "कर्मधारयः-3" : "कर्मधारयः",
    "कर्मधारयः-4" : "कर्मधारयः",
    "कर्मधारयः-5" : "कर्मधारयः",
    "-" : "तत्पुरुषः",
}

gold_map = {
    "बहुव्रीहिः" : "बहुव्रीहिः",
    "षष्ठी-तत्पुरुषः" : "षष्ठी-तत्पुरुषः",
    "नञ्-तत्पुरुषः" : "नञ्-तत्पुरुषः",
    "कर्मधारयः" : "कर्मधारयः",
    "इतरेतर-द्वन्द्वः" : "द्वन्द्वः",
    "उपपद-तत्पुरुषः" : "उपपद-तत्पुरुषः",
    "तृतीया-तत्पुरुषः" : "तृतीया-तत्पुरुषः",
    "सप्तमी-तत्पुरुषः" : "सप्तमी-तत्पुरुषः",
    "द्वन्द्वः" : "द्वन्द्वः",
    "अव्ययीभावः" : "अव्ययीभावः",
    "पञ्चमी-तत्पुरुषः" : "पञ्चमी-तत्पुरुषः",
    "नञ्_तत्पुरुषः" : "नञ्-तत्पुरुषः",
    "नञ्‌-तत्पुरुषः" : "नञ्-तत्पुरुषः",
    "नञ्-तत्पुरुष" : "नञ्-तत्पुरुषः",
    "तत्पुरुषः" : "तत्पुरुषः",
    "उपपद_तत्पुरुषः" : "उपपद-तत्पुरुषः",
    "षष्ठी_तत्पुरुषः" : "षष्ठी-तत्पुरुषः",
    "प्रादि-तत्पुरुषः" : "तत्पुरुषः",
    "द्वन्दः" : "द्वन्द्वः",
    "चतुर्थी-तत्पुरुषः" : "चतुर्थी-तत्पुरुषः",
    "द्वितीया-तत्पुरुषः" : "द्वितीया-तत्पुरुषः",
    "समाहार-द्वन्द्वः" : "द्वन्द्वः",
    "नञ्-बहुव्रीहिः" : "नञ्-बहुव्रीहिः",
    "सप्तमी_तत्पुरुषः" : "सप्तमी-तत्पुरुषः",
    "षष्ठी-तत्पुरुष" : "षष्ठी-तत्पुरुषः",
    "तृतीया_तत्पुरुषः" : "तृतीया-तत्पुरुषः",
    "इतरेतर_द्वन्द्वः" : "द्वन्द्वः",
    "षष्ठी-तत्पुरुषः-" : "षष्ठी-तत्पुरुषः",
    "केवल-समासः" : "केवल-समासः",
    "उपपद-तत्पुरुष" : "उपपद-तत्पुरुषः",
    "इतरेतर-द्वन्दः" : "द्वन्द्वः",
    "षष्ठी-सम्बन्धः" : "षष्ठी-तत्पुरुषः",
    "प्रादि-समासः" : "तत्पुरुषः",
    "द्वितीया_तत्पुरुषः" : "द्वितीया-तत्पुरुषः",
    "कर्मधारय" : "कर्मधारयः",
    "उपपदसमासः" : "उपपद-तत्पुरुषः",
    "उपपद-समासः" : "उपपद-तत्पुरुषः",
    "सुप्-समुच्चितः" : "द्वन्द्वः",
    "सम्बन्धः" : "तत्पुरुषः",
    "प्रादि_तत्पुरुषः" : "तत्पुरुषः",
    "पञ्चमी_तत्पुरुषः" : "पञ्चमी-तत्पुरुषः",
    "पञ्च-तत्पुरुषः" : "पञ्चमी-तत्पुरुषः",
    "नञ्_बहुव्रीहिः" : "नञ्-बहुव्रीहिः",
    "द्विगु-तत्पुरुषः" : "द्विगु-तत्पुरुषः",
    "तॄतीया-तत्पुरुषः" : "तृतीया-तत्पुरुषः",
    "चतुर्थी_तत्पुरुषः" : "चतुर्थी-तत्पुरुषः",
    "केवल_समासः" : "केवल-समासः",
    "कर्मप्रवचनीयः" : "अव्ययीभावः",
    "इतरेतरद्वन्द्वः" : "द्वन्द्वः",
    "नञ्-तत्पुरुष" : "नञ्-तत्पुरुषः",
}


def get_code_for_relation(relation):
    """ """
    
    return cpd_codes.get(relation, relation)
    

def get_code_for_relation_2(relation):
    """ """
    
    return cpd_codes_2.get(relation, relation)


def read_contents(name_):
    """ """
    
    file_ = open(name_, "r", encoding="utf-8")
    file_contents = file_.read()
    file_.close()
    
    file_lines = list(filter(None, file_contents.split("\n")))
    
    return file_lines[1:]        
    

def call_anusaaraka(encoding, splitter, out_encoding, parse,
                    text_type, tlang, mode, text, cpd_analysis):
    """ """
    
#    out_enc = output_encoding if output_encoding in ["roma", "deva"] else "roma"
    
    env_vars = [
        "encoding=" + encoding,
        "splitter=" + splitter,
        "out_encoding=" + out_encoding,
        "parse=" + parse,
        "text_type=" + text_type,#.replace(" ", "+"),
        "tlang=" + tlang,
        "mode=" + mode,
        "compound_analysis=" + cpd_analysis,
        "text=" + text,
    ]
    
    query_string = "QUERY_STRING=\"" + "&".join(env_vars) + "\""
    command = query_string + " " + cgi_file
    
    original_cwd = os.getcwd()
    os.chdir("/usr/lib/cgi-bin/scl/MT")
    
    print(command)
    
    try:
        p = sp.Popen(command, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
        outs, errs = p.communicate()
    except Exception as e:
        result = ""
        status = "Failed: " + str(e)
        # print("Exception: " + status)
    else:
        result = outs.decode('utf-8')
        status = "Success"
        error = errs.decode('utf-8')
        # print("Result: " + result)
        # print("Error: " + error)
    finally:
        # Restore the original working directory
        os.chdir(original_cwd)
    
    return result, status, error


def get_compound_annotation(dep_res_json_str):
    """ """
    
    dep_res_json_str = dep_res_json_str.split("\n")[-1]
    dep_res_json = json.loads(dep_res_json_str)
    annotated_sentences = []
    for sent_json in dep_res_json:
        words_analysis = sent_json["sent"]
        word_rel = []
        for word_json in words_analysis:
            index = word_json["anvaya_no"]
            word = word_json["word"]
            rel = word_json["kaaraka_sambandha"]
            if ";" in rel:
                rel = rel.split(";")[0]
            if "#" in rel:
                rel = rel.split("#")[0]
            if "," in rel:
                rel_type, rel_index = rel.split(",")
                rel_type = rel_type.replace("_", "-")
                rel = f"{get_code_for_relation(rel_type)},{rel_index}"
            word_rel.append((index, word, rel))
        
        annotated_sentences.append(word_rel)
    
    return annotated_sentences[0] if len(annotated_sentences) > 0 else []


def handle_xvanxva(annotated_sentence):
    """ """
    
    new_details = []
    cur_word_index = 1
    cur_cpd_index = 1
    is_cpd = False
    index_changes = {}
    for index, word, rel in annotated_sentence:
        new_index = ""
        if not rel or rel == "-" or "," not in rel:
            rel = "-,-"
        
        if "_" in word:
            d_cmpnts = word.split("_")
            w = 0
            while w < len(d_cmpnts):
                dc = d_cmpnts[w]
                new_cmpnt = f"{dc}-" if w < len(d_cmpnts) - 1 else dc
                new_index = f"{str(cur_word_index)}.{str(cur_cpd_index)}"
                if w < len(d_cmpnts) - 1:
                    new_cmpnt = f"{dc}-"
                    new_relation = f"इतरेतर-द्वन्द्वः,{str(cur_word_index)}.{str(cur_cpd_index + len(d_cmpnts) - w - 1)}"
                    updated = "new"
                else:
                    new_cmpnt = dc
                    new_relation = rel
                    updated = "old"
                new_details.append((index, new_index, new_cmpnt, new_relation, updated))
                cur_cpd_index += 1
                w += 1
#            dc = d_cmpnts[w]
#            new_cmpnt = f"{dc}"
#            new_index = f"{str(cur_word_index)}.{str(cur_cpd_index)}"
#            new_details.append((index, new_index, new_cmpnt, rel))
            if "-" in word:
                is_cpd = True
        elif "-" in word:
            new_index = f"{str(cur_word_index)}.{str(cur_cpd_index)}"
            new_details.append((index, new_index, word, rel, "old"))
            is_cpd = True
            cur_cpd_index += 1
            # For multiple relations
            if "#" in rel:
                rel = rel.split("#")[0]
            rel_type, rel_index = rel.split(",")
        elif is_cpd and "-" not in word:
            new_index = f"{str(cur_word_index)}.{str(cur_cpd_index)}"
            new_details.append((index, new_index, word, rel, "old"))
            cur_word_index += 1
            cur_cpd_index = 1
            is_cpd = False
        else:
            new_index = f"{str(cur_word_index)}.{str(cur_cpd_index)}"
            new_details.append((index, new_index, word, rel, "old"))
            cur_word_index += 1
            cur_cpd_index = 1
            is_cpd = False
        
        index_changes[index] = new_index
    
    new_details_updated = []
    for old_index, new_index, word, rel, updated in new_details:
        if not rel or rel == "-":
            new_details_updated.append((new_index, word, rel))
            break
        if "#" in rel:
            rel = rel.split("#")[0]
        rel_type, rel_index = rel.split(",")
        if rel_index in index_changes and updated == "old":
            new_rel = f"{rel_type},{index_changes[rel_index]}"
            new_details_updated.append((new_index, word, new_rel))
        else:
            new_details_updated.append((new_index, word, rel))
    
    return new_details_updated


def test(sentence, encoding):
    """ """
    
    splitter = "None"
    out_encoding = "Devanagari"
    parse = "full"
    text_type = "Sloka"
    tlang = "Hindi"
    mode = "json"
    cpd_analysis = "YES"
    
    res, status, error = call_anusaaraka(
        encoding, splitter, out_encoding, 
        parse, text_type, tlang, mode, 
        sentence, cpd_analysis
    )
    
    return res, status, error
    

def evaluation(gold_analysis, pred_analysis, grain="fine"):
    """ """
    
    rel_type_matches = 0.0
    rel_index_matches = 0.0
    
    complete_rel_matches = 0.0

    no_analysis = 0
    
    gold_pred_pairs = []
    
    for j in range(len(gold_analysis) - 1):
        gold_index, gold_word, gold_relation = gold_analysis[j]
        pred_index, pred_word, pred_relation = pred_analysis[j]
        
        if "-" in gold_word:
            gold_rel_type, gold_rel_index = gold_relation.split(",")
            pred_rel_type, pred_rel_index = pred_relation.split(",")
            
            if not pred_rel_type or pred_rel_type == "-":
                no_analysis += 1

            gold_rel_type = gold_rel_type.rstrip("-")
            
            gold_rel_type = gold_map.get(gold_rel_type, gold_rel_type)
            
            if grain == "coarse":
                gold_rel_type = fine_to_coarse_dev[gold_rel_type]
                pred_rel_type = fine_to_coarse_dev.get(pred_rel_type, pred_rel_type)
            
#            pred_rel_type = pred_rel_type.replace("_", "-")
            
            if gold_rel_type == pred_rel_type:
                rel_type_matches += 1
                gold_pred_pairs.append((gold_rel_type, pred_rel_type))
            elif gold_rel_type == get_code_for_relation(pred_rel_type) or (grain == "coarse" and gold_rel_type == fine_to_coarse_dev[get_code_for_relation(pred_rel_type)]):
                rel_type_matches += 1
                gold_pred_pairs.append((gold_rel_type, fine_to_coarse_dev[get_code_for_relation(pred_rel_type)]))
            elif gold_rel_type == get_code_for_relation_2(pred_rel_type) or (grain == "coarse" and gold_rel_type == fine_to_coarse_dev[get_code_for_relation_2(pred_rel_type)]):
                rel_type_matches += 1
                gold_pred_pairs.append((gold_rel_type, fine_to_coarse_dev[get_code_for_relation_2(pred_rel_type)]))
            else:
                gold_pred_pairs.append((gold_rel_type, pred_rel_type))
            
#            gold_pred_pairs.append((gold_rel_type, pred_rel_type, get_code_for_relation(pred_rel_type), get_code_for_relation_2(pred_rel_type)))
            
            if grain == "coarse":
                modified_pred_relation_1 = f"{fine_to_coarse_dev[get_code_for_relation(pred_rel_type)]},{pred_rel_index}"
                modified_pred_relation_2 = f"{fine_to_coarse_dev[get_code_for_relation_2(pred_rel_type)]},{pred_rel_index}"
            else:
                modified_pred_relation_1 = f"{get_code_for_relation(pred_rel_type)},{pred_rel_index}"
                modified_pred_relation_2 = f"{get_code_for_relation_2(pred_rel_type)},{pred_rel_index}"
            
            modified_gold_relation = f"{gold_rel_type},{gold_rel_index}"
            
            if gold_rel_index == pred_rel_index:
                rel_index_matches += 1
            
            if gold_relation == pred_relation:
                complete_rel_matches += 1
            elif modified_gold_relation == modified_pred_relation_1:
                complete_rel_matches += 1
            elif modified_gold_relation == modified_pred_relation_2:
                complete_rel_matches += 1
            
#            print(rel_type_matches, rel_index_matches, complete_rel_matches)
    
    # The last word is an auxiliary verb for making the parser working
    # Hence it is not included. The last component will anyhow be marked 
    # with a word outside of the compound and hence not considered
    no_of_components_to_be_considered = len(gold_analysis) - 2
    
    rel_type_score = rel_type_matches / no_of_components_to_be_considered
    rel_index_score = rel_index_matches / no_of_components_to_be_considered
    complete_rel_score = complete_rel_matches / no_of_components_to_be_considered
    
#    print("Score: ", rel_type_score, rel_index_score, complete_rel_score)
    
    return rel_type_score, rel_index_score, complete_rel_score, no_analysis == 0, gold_pred_pairs
            

def test_sample(sentence, encoding):
    """ """
    
    res, status, error = test(sentence, encoding)
    print(res, status, error)
    pred_analysis = get_compound_annotation(res)
#    converted_analysis = handle_xvanxva(pred_analysis)
    print("\n".join(["\t".join(x) for x in pred_analysis]))


def run_all(gold_compounds, encoding):
    """ """
    
    errors = []
    rel_type_scores = []
    rel_index_scores = []
    complete_rel_scores = []
    
    results = []
    gold_pred_pairs = []
    
    for i in tqdm(range(len(gold_compounds))):
        print(gold_compounds[i])
        
        id_, line, gold_analysis = gold_compounds[i]

        compound = line.split(" ")[0]
        
        res, status, error = test(line, encoding)
        
        if error or not status == "Success":
            errors.append((id_, compound, gold_analysis))
            # results.append((id_, compound, gold_analysis, "Failure", error, "", "", ""))
            # rel_type_scores.append(0.0)
            # rel_index_scores.append(0.0)
            # complete_rel_scores.append(0.0)
            # continue
        
        print("Text: " + line, "Result: " + res)
        pred_analysis = get_compound_annotation(res)
        converted_analysis = handle_xvanxva(pred_analysis)
        
        gold_analysis_str = json.dumps(gold_analysis)
        
        # print(gold_analysis)
        # print(converted_analysis)
        
        rel_type_score, rel_index_score, complete_rel_score, no_analysis, cur_gold_pred_pairs = evaluation(gold_analysis, converted_analysis)
        gold_pred_pairs += cur_gold_pred_pairs
        
        results.append((id_, compound, gold_analysis, "Success", converted_analysis, str(no_analysis), str(rel_type_score), str(rel_index_score), str(complete_rel_score)))
        
        rel_type_scores.append(rel_type_score)
        rel_index_scores.append(rel_index_score)
        complete_rel_scores.append(complete_rel_score)
        
        print(rel_type_scores, rel_index_scores, complete_rel_scores)
        
    
    print(rel_type_scores, rel_index_scores, complete_rel_scores)
    
    avg_rel_type_score = np.mean(rel_type_scores)*100.0
    avg_rel_index_score = np.mean(rel_index_scores)*100.0
    avg_complete_rel_score = np.mean(complete_rel_scores)*100.0
    
    scores = {
        "avg_rel_type_score" : avg_rel_type_score,
        "avg_rel_index_score" : avg_rel_index_score,
        "avg_complete_rel_score" : avg_complete_rel_score,
    }
    
    return scores, errors, results, gold_pred_pairs
        
