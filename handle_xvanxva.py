import sys
import json

script, in_, out_ = sys.argv

def read_contents(name_):
    """ """
    
    file_ = open(name_, "r", encoding="utf-8")
    file_contents = file_.read()
    file_.close()
    
    file_lines = list(filter(None, file_contents.split("\n")))
    
    return file_lines[:]
    

def get_compound_annotation(dep_res_json_str):
    """ """
    
    dep_res_json = json.loads(dep_res_json_str)
    annotated_sentences = []
    for sent_json in dep_res_json:
        words_analysis = sent_json["sent"]
        word_rel = []
        for word_json in words_analysis:
            index = word_json["index"]
            word = word_json["word"]
            rel = word_json["kaaraka_sambandha"]
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
        if rel == "-":
            new_details_updated.append((new_index, word, rel))
            break
        rel_type, rel_index = rel.split(",")
        if rel_index in index_changes and updated == "old":
            new_rel = f"{rel_type},{index_changes[rel_index]}"
            new_details_updated.append((new_index, word, new_rel))
        else:
            new_details_updated.append((new_index, word, rel))
    
    return new_details_updated
    

#res_json_str = '[{"sent":[{"index":"1.1","word":"ज्ञान_योग-","poem":"","sandhied_word":"ज्ञान_योग-व्यवस्थितिः","morph_analysis":"ज्ञान_योग","morph_in_context":"ज्ञान_योग","kaaraka_sambandha":"त_पु_6,1.2","possible_relations":"त_पु_6,1.2","color_code":"#FFFF00","hindi_meaning":"","hindi_meaning_active":"ज्ञान_योग-"},{"index":"1.2","word":"व्यवस्थितिः","poem":"","sandhied_word":"--","morph_analysis":"व्यवस्थिति{स्त्री;1;एक}","morph_in_context":"व्यवस्थिति{स्त्री;1;एक}","kaaraka_sambandha":"कर्ता,2.1","possible_relations":"कर्ता_बे_वेर्ब्स्,2.1","color_code":"#00BFFF","hindi_meaning":"","hindi_meaning_active":"क्रमबन्धन"},{"index":"2.1","word":"अस्ति","poem":"","sandhied_word":"अस्ति","morph_analysis":"अस्2{कर्तरि;लट्;प्र;एक;परस्मैपदी;अदादिः}","morph_in_context":"अस्2{कर्तरि;लट्;प्र;एक;परस्मैपदी;अदादिः}","kaaraka_sambandha":"अभिहित_कर्ता,1.2","possible_relations":"-","color_code":"#FF1975","hindi_meaning":"","hindi_meaning_active":"है"},{"index":"3.1","word":".","poem":"","sandhied_word":".","morph_analysis":"-","morph_in_context":"-","kaaraka_sambandha":"-","possible_relations":"-","color_code":"","hindi_meaning":"","hindi_meaning_active":"-"}]}]'

#annotations = get_compound_annotation(res_json_str)

lines = read_contents(in_)

annotations = [ x.split("\t") for x in lines ]

print("Before:")
print("\n".join([ "\t".join(x) for x in annotations ]))

new_annotations = handle_xvanxva(annotations)

print("\nAfter:")
print("\n".join([ "\t".join(x) for x in new_annotations ]))

out_f = open(out_, "w", encoding="utf-8")
out_f.write("\n".join(([ "\t".join(x) for x in new_annotations ])))
out_f.close()
