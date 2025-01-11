import os
import sys

import subprocess as sp

import json
import numpy as np

from tqdm import tqdm

import devtrans


cgi_file = "/usr/lib/cgi-bin/scl_cpd/MT/anusaaraka.cgi"


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
    "क_धा_1" : "कर्मधारयः",
    "क_धा_2" : "कर्मधारयः",
    "क_धा_3" : "कर्मधारयः",
    "क_धा_4" : "कर्मधारयः",
    "क_धा_5" : "कर्मधारयः",
    "ब_व्री" : "बहुव्रीहिः",
    "अ_भा" : "अव्ययीभावः",
    "द्वन्द्वः" : "इतरेत-द्वन्द्वः",
}

def get_code_for_relation(relation):
    """ """
    
    return cpd_codes.get(relation, relation)


def read_contents(name_):
    """ """
    
    file_ = open(name_, "r", encoding="utf-8")
    file_contents = file_.read()
    file_.close()
    
    file_lines = list(filter(None, file_contents.split("\n")))
    
    return file_lines[1:]


def get_cpds(lines):
    """ """
    
    cpds = []
    for line in lines:
        items = line.split("\t")
        index = items[0]
        word = items[1]
        kAraka_sambanXa = items[6]
        
        if "-" in word or "_" in word:
            cpds.append(word, kAraka_sambanXa)
            
    return cpds


def compare_with_gold(gold_tsv, pred_tsv):
    """ """
    
    gold_lines = read_contents(gold_tsv)
    pred_lines = read_contents(pred_tsv)
    
    p = 0
    for g in gold_lines:
        g_items = gold_lines[g].split("\t")
        g_index = g_items[0]
        g_word = g_items[1]
        
        p_items = pred_lines[p].split("\t")
        p_index = p_items[0]
        p_word = p_items[1]
        
#        if p_word == g_word:
#            
    

def call_anusaaraka(encoding, splitter, out_encoding, parse,
                    text_type, tlang, mode, text):
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
        "text=" + text,
    ]
    
    query_string = "QUERY_STRING=\"" + "&".join(env_vars) + "\""
    command = query_string + " " + cgi_file
    
    original_cwd = os.getcwd()
    os.chdir("/usr/lib/cgi-bin/scl_cpd/MT")
    
#    print(command)
    
    try:
        p = sp.Popen(command, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
        outs, errs = p.communicate()
    except Exception as e:
        result = ""
        status = "Failure: " + str(e)
    else:
        result = outs.decode('utf-8')
        status = "Success"
        error = errs.decode('utf-8')
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
            index = word_json["index"]
            word = word_json["word"]
            rel = word_json["kaaraka_sambandha"]
            if ";" in rel:
                rel = rel.split(";")[0]
            if "," in rel:
                rel_type, rel_index = rel.split(",")
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
            rel_type, rel_index = rel.split(",")
            rel_w_index, rel_c_index = rel_index.split(".")
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
    
    res, status, error = call_anusaaraka(
        encoding, splitter, out_encoding, 
        parse, text_type, tlang, mode, sentence
    )
    
    return res, status, error
    

def evaluation(gold_analysis, pred_analysis):
    """ """
    
    rel_type_matches = 0.0
    rel_index_matches = 0.0
    
    complete_rel_matches = 0.0
    
    for j in range(len(gold_analysis) - 1):
        gold_index, gold_word, gold_relation = gold_analysis[j]
        pred_index, pred_word, pred_relation = pred_analysis[j]
        
        if "-" in gold_word:
            gold_rel_type, gold_rel_index = gold_relation.split(",")
            pred_rel_type, pred_rel_index = pred_relation.split(",")
            
#            print(gold_rel_type, gold_rel_index)
#            print(pred_rel_type, pred_rel_index)
            
            if gold_rel_type == pred_rel_type:
                rel_type_matches += 1
            elif gold_rel_type == get_code_for_relation(pred_rel_type):
                rel_type_matches += 1
            
            if gold_rel_index == pred_rel_index:
                rel_index_matches += 1
            
            modified_pred_relation = f"{get_code_for_relation(pred_rel_type),pred_rel_index}"
            if gold_relation == modified_pred_relation:
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
    
    return rel_type_score, rel_index_score, complete_rel_score
            
    
def run_all(gold_compounds, encoding):
    """ """
    
    errors = []
    rel_type_scores = []
    rel_index_scores = []
    complete_rel_scores = []
    
    for i in tqdm(range(len(gold_compounds))):
        id_, line, gold_analysis = gold_compounds[i]
        
        res, status, error = test(line, encoding)
        
        if error or not status == "Success":
            errors.append(gold_compounds[i])
            continue
        
        pred_analysis = get_compound_annotation(res)
        converted_analysis = handle_xvanxva(pred_analysis)
        
#        print(gold_analysis)
#        print(pred_analysis)
        
        rel_type_score, rel_index_score, complete_rel_score = evaluation(gold_analysis, converted_analysis)
        rel_type_scores.append(rel_type_score)
        rel_index_scores.append(rel_index_score)
        complete_rel_scores.append(complete_rel_score)
        
#        print(rel_type_scores, rel_index_scores, complete_rel_scores)
        
    
#    print(rel_type_scores, rel_index_scores, complete_rel_scores)
    
    avg_rel_type_score = np.mean(rel_type_scores)*100.0
    avg_rel_index_score = np.mean(rel_index_scores)*100.0
    avg_complete_rel_score = np.mean(complete_rel_scores)*100.0
    
    overall_result = {
        "avg_rel_type_score" : avg_rel_type_score,
        "avg_rel_index_score" : avg_rel_index_score,
        "avg_complete_rel_score" : avg_complete_rel_score,
    }
    
    return overall_result, errors
        
