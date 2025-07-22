import os
import sys

import subprocess as sp

import json
import numpy as np

from tqdm import tqdm

import devtrans

from evaluate import *

script, in_, out_, res, grain_ = sys.argv


fine_to_coarse = {
    "avyayībhāvaḥ" : "avyayībhāvaḥ",
    "itaretara-dvandvaḥ" : "dvandvaḥ",
    "upapada-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "karmadhārayaḥ" : "tatpuruṣaḥ",
    "kevala-samāsaḥ" : "tatpuruṣaḥ",
    "caturthī-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "tatpuruṣaḥ" : " tatpuruṣaḥ",
    "tṛtīyā-tatpuruṣaḥ" : " tatpuruṣaḥ",
    "dvandvaḥ" : " dvandvaḥ",
    "dvitīyā-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "nañ-tatpuruṣaḥ" : "  tatpuruṣaḥ",
    "nañ-bahuvrīhiḥ" : "  bahuvrīhiḥ",
    "pañcamī-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "prādi-tatpuruṣaḥ" : " tatpuruṣaḥ",
    "bahuvrīhiḥ" : " bahuvrīhiḥ",
    "ṣaṣṭhī-tatpuruṣaḥ" : " tatpuruṣaḥ",
    "saptamī-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "upamānam" : "tatpuruṣaḥ",
    "dvigu-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "-" : "-",
}


def eval_cpds(details):
    """ """
    
    rel_type_scores = []
    rel_index_scores = []
    complete_rel_scores = []
    
    results = []
    
    for det in tqdm(details):
        # print(det)
        id_, compound, gold_analysis_str, status, predicted_analysis_str, _, _, _, _ = det.split("\t")
        
        count = str(compound.count("-"))
        if not count == "1":
            continue
        
        gold_analysis = json.loads(gold_analysis_str)
        converted_analysis = json.loads(predicted_analysis_str)
        
        rel_type_score, rel_index_score, complete_rel_score, no_analysis, gold_pred_pairs = evaluation(gold_analysis, converted_analysis, grain_)
        
        print(rel_type_score, rel_index_score, complete_rel_score, no_analysis, gold_pred_pairs)
        
        results.append("\t".join((str(id_), compound, count, json.dumps(gold_analysis, ensure_ascii=False), status, json.dumps(converted_analysis, ensure_ascii=False), str(no_analysis), str(rel_type_score), str(rel_index_score), str(complete_rel_score))))
        
        rel_type_scores.append(rel_type_score)
        rel_index_scores.append(rel_index_score)
        complete_rel_scores.append(complete_rel_score)
        
    avg_rel_type_score = np.mean(rel_type_scores)*100.0
    avg_rel_index_score = np.mean(rel_index_scores)*100.0
    avg_complete_rel_score = np.mean(complete_rel_scores)*100.0
    
    scores = {
        "avg_rel_type_score" : avg_rel_type_score,
        "avg_rel_index_score" : avg_rel_index_score,
        "avg_complete_rel_score" : avg_complete_rel_score,
    }
    
#    print(results)
#    results_str = [ "\t".join(item) for item in results ]
    
    return scores, results


in_lines = read_contents(in_)
scores, results = eval_cpds(in_lines)
out_file = open(out_, "w", encoding="utf-8")
out_file.write("\n".join(results))
out_file.close()

with open(res, "w", encoding="utf-8") as f:
    f.write(json.dumps(scores, ensure_ascii=False))
