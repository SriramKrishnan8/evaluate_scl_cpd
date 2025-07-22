import os
import sys

import json

script, in_, out_, ph = sys.argv


avyayIBAva_phases = [
    "Iiy"
]

bahuvrIhi_phases = [
    "Ifc", "Ifcc", "Ifcv"
]


def check_cpd(morphs, g_word, phases):
    """ """
    
    found = False
    for m in morphs:
        word = m.get("word", "")
        word = word.replace("-", "")
        phase = m.get("phase", "")
        
        if g_word == word:
            if phase in phases:
                found = True
                break
    
    return found


in_file = open(in_, "r", encoding="utf-8")
in_contents = in_file.read()
in_file.close()

in_lines = list(filter(None, in_contents.split("\n")))

new_lines = []

if ph == "ab":
    phases = avyayIBAva_phases
elif ph == "bv":
    phases = bahuvrIhi_phases

for line in in_lines[:]:
    items = line.split("\t")
    compound = items[0]
    segments = items[1]
    
    sh_out_json = json.loads(items[2])
    
#    compound = sh_out_json.get("input", "")
    status = sh_out_json.get("status", "")
    if status in [ "failure", "unrecognized" ]:
        new_lines.append("\t".join((items + [ status, status ])))
        continue
    segmentation = sh_out_json.get("segmentation", "")
    morphs = sh_out_json.get("morph", "")
    
    found = False
    for sgmnt in segments.split("-"):
        found = check_cpd(morphs, sgmnt, phases)
        if found:
            break
    
#    if found:
#        new_lines.append("\t".join((items + [ "True" ])))
#    else:
#        new_lines.append("\t".join((items + [ "False" ])))
        
    result = "found" if found else "not found"
    segmentation_found = "found" if segments in segmentation else "not found"
    new_lines.append("\t".join((items + [ segmentation_found, result ])))

out_file = open(out_, "w", encoding="utf-8")
out_file.write("\n".join(new_lines))
out_file.close()
