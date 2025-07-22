import sys

import pandas as pd

import devtrans as dt

script, in_, conf_fine, conf_course, class_fine, class_course = sys.argv


def replace_underscores(lst_):
    """
    Replace underscores with hyphens in a list of strings.
    """

    return [item.replace("_", "-") for item in lst_]

# Load TSV file
df = pd.read_csv(in_, sep="\t", header=None, names=["gold", "pred"], encoding="utf-8")

gold_fine = [ dt.dev2iast(item) for item in df["gold"].tolist() ]
pred_fine = [ dt.dev2iast(item) for item in df["pred"].tolist() ]

gold_fine = replace_underscores(gold_fine)
pred_fine = replace_underscores(pred_fine)

fine_to_coarse_dev = {
    "बहुव्रीहिः" : "बहुव्रीहिः",
    "षष्ठी-तत्पुरुषः" : "तत्पुरुषः",
    "नञ्-तत्पुरुषः" : "तत्पुरुषः",
    "कर्मधारयः" : "कर्मधारयः",
    "इतरेतर-द्वन्द्वः" : "द्वन्द्वः",
    "उपपद-तत्पुरुषः" : "तत्पुरुषः",
    "तृतीया-तत्पुरुषः" : "तत्पुरुषः",
    "सप्तमी-तत्पुरुषः" : "तत्पुरुषः",
    "द्वन्द्वः" : "द्वन्द्वः",
    "अव्ययीभावः" : "अव्ययीभावः",
    "पञ्चमी-तत्पुरुषः" : "तत्पुरुषः",
    "नञ्_तत्पुरुषः" : "तत्पुरुषः",
    "नञ्‌-तत्पुरुषः" : "तत्पुरुषः",
    "नञ्-तत्पुरुष" : "तत्पुरुषः",
    "तत्पुरुषः" : "तत्पुरुषः",
    "उपपद_तत्पुरुषः" : "तत्पुरुषः",
    "षष्ठी_तत्पुरुषः" : "तत्पुरुषः",
    "प्रादि-तत्पुरुषः" : "तत्पुरुषः",
    "द्वन्दः" : "द्वन्द्वः",
    "चतुर्थी-तत्पुरुषः" : "तत्पुरुषः",
    "द्वितीया-तत्पुरुषः" : "तत्पुरुषः",
    "समाहार-द्वन्द्वः" : "द्वन्द्वः",
    "नञ्-बहुव्रीहिः" : "बहुव्रीहिः",
    "सप्तमी_तत्पुरुषः" : "तत्पुरुषः",
    "षष्ठी-तत्पुरुष" : "तत्पुरुषः",
    "तृतीया_तत्पुरुषः" : "तत्पुरुषः",
    "इतरेतर_द्वन्द्वः" : "द्वन्द्वः",
    "षष्ठी-तत्पुरुषः-" : "तत्पुरुषः",
    "केवल-समासः" : "केवल-समासः",
    "उपपद-तत्पुरुष" : "तत्पुरुषः",
    "इतरेतर-द्वन्दः" : "द्वन्द्वः",
    "षष्ठी-सम्बन्धः" : "तत्पुरुषः",
    "प्रादि-समासः" : "तत्पुरुषः",
    "द्वितीया_तत्पुरुषः" : "तत्पुरुषः",
    "कर्मधारय" : "कर्मधारयः",
    "उपपदसमासः" : "तत्पुरुषः",
    "उपपद-समासः" : "तत्पुरुषः",
    "सुप्-समुच्चितः" : "द्वन्द्वः",
    "सम्बन्धः" : "तत्पुरुषः",
    "प्रादि_तत्पुरुषः" : "तत्पुरुषः",
    "पञ्चमी_तत्पुरुषः" : "तत्पुरुषः",
    "पञ्च-तत्पुरुषः" : "तत्पुरुषः",
    "नञ्_बहुव्रीहिः" : "बहुव्रीहिः",
    "द्विगु-तत्पुरुषः" : "तत्पुरुषः",
    "तॄतीया-तत्पुरुषः" : "तत्पुरुषः",
    "चतुर्थी_तत्पुरुषः" : "तत्पुरुषः",
    "केवल_समासः" : "केवल-समासः",
    "कर्मप्रवचनीयः" : "अव्ययीभावः",
    "इतरेतरद्वन्द्वः" : "द्वन्द्वः",
    "नञ्-तत्पुरुष" : "तत्पुरुषः",
}

fine_to_coarse = {
    "bahuvrīhiḥ" : "bahuvrīhiḥ",
    "ṣaṣṭhī-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "nañ-tatpuruṣaḥ" : "tatpuruṣaḥ",
    # "karmadhārayaḥ" : "karmadhārayaḥ",
    "karmadhārayaḥ" : "tatpuruṣaḥ",
    "itaretara-dvandvaḥ" : "dvandvaḥ",
    "prathamā-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "upapada-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "tṛtīyā-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "saptamī-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "dvandvaḥ" : "dvandvaḥ",
    "avyayībhāvaḥ" : "avyayībhāvaḥ",
    "pañcamī-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "nañ_tatpuruṣaḥ" : "tatpuruṣaḥ",
    "nañ-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "nañ-tatpuruṣa" : "tatpuruṣaḥ",
    "tatpuruṣaḥ" : "tatpuruṣaḥ",
    "upapada_tatpuruṣaḥ" : "tatpuruṣaḥ",
    "ṣaṣṭhī_tatpuruṣaḥ" : "tatpuruṣaḥ",
    "prādi-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "dvandaḥ" : "dvandvaḥ",
    "caturthī-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "dvitīyā-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "samāhāra-dvandvaḥ" : "dvandvaḥ",
    "nañ-bahuvrīhiḥ" : "bahuvrīhiḥ",
    "saptamī_tatpuruṣaḥ" : "tatpuruṣaḥ",
    "ṣaṣṭhī-tatpuruṣa" : "tatpuruṣaḥ",
    "tṛtīyā_tatpuruṣaḥ" : "tatpuruṣaḥ",
    "itaretara_dvandvaḥ" : "dvandvaḥ",
    "ṣaṣṭhī-tatpuruṣaḥ-" : "tatpuruṣaḥ",
    # "kevala-samāsaḥ" : "kevala-samāsaḥ",
    "kevala-samāsaḥ" : "tatpuruṣaḥ",
    "upapada-tatpuruṣa" : "tatpuruṣaḥ",
    "itaretara-dvandaḥ" : "dvandvaḥ",
    "ṣaṣṭhī-sambandhaḥ" : "tatpuruṣaḥ",
    "prādi-samāsaḥ" : "tatpuruṣaḥ",
    "dvitīyā_tatpuruṣaḥ" : "tatpuruṣaḥ",
    # "karmadhāraya" : "karmadhārayaḥ",
    "karmadhāraya" : "tatpuruṣaḥ",
    "upapadasamāsaḥ" : "tatpuruṣaḥ",
    "upapada-samāsaḥ" : "tatpuruṣaḥ",
    "sup-samuccitaḥ" : "dvandvaḥ",
    "sambandhaḥ" : "tatpuruṣaḥ",
    "prādi_tatpuruṣaḥ" : "tatpuruṣaḥ",
    "pañcamī_tatpuruṣaḥ" : "tatpuruṣaḥ",
    "pañca-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "nañ_bahuvrīhiḥ" : "bahuvrīhiḥ",
    "dvigu-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "tṝtīyā-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "caturthī_tatpuruṣaḥ" : "tatpuruṣaḥ",
    # "kevala_samāsaḥ" : "kevala-samāsaḥ",
    "kevala_samāsaḥ" : "tatpuruṣaḥ",
    "karmapravacanīyaḥ" : "avyayībhāvaḥ",
    "itaretaradvandvaḥ" : "dvandvaḥ",
    "nañ-tatpuruṣa" : "tatpuruṣaḥ",
    # "karmadhārayaḥ-1" : "karmadhārayaḥ",
    # "karmadhārayaḥ-2" : "karmadhārayaḥ",
    # "karmadhārayaḥ-3" : "karmadhārayaḥ",
    # "karmadhārayaḥ-4" : "karmadhārayaḥ",
    # "karmadhārayaḥ-5" : "karmadhārayaḥ",
    "karmadhārayaḥ-1" : "tatpuruṣaḥ",
    "karmadhārayaḥ-2" : "tatpuruṣaḥ",
    "karmadhārayaḥ-3" : "tatpuruṣaḥ",
    "karmadhārayaḥ-4" : "tatpuruṣaḥ",
    "karmadhārayaḥ-5" : "tatpuruṣaḥ",
    "avyayībhāvaḥ-1" : "avyayībhāvaḥ",
    "avyayībhāvaḥ-2" : "avyayībhāvaḥ",
    "avyayībhāvaḥ-3" : "avyayībhāvaḥ",
    "avyayībhāvaḥ-4" : "avyayībhāvaḥ",
    "avyayībhāvaḥ-5" : "avyayībhāvaḥ",
    "avyayībhāvaḥ-6" : "avyayībhāvaḥ",
    "avyayībhāvaḥ-7" : "avyayībhāvaḥ",
    # "-" : "-",
    "-" : "tatpuruṣaḥ",
    "upamānam" : "tatpuruṣaḥ",
}

gold_coarse = [fine_to_coarse.get(label, label) for label in gold_fine]
pred_coarse = [fine_to_coarse.get(label, label) for label in pred_fine]

print("gold course -> ", set(gold_coarse))

print("pred course -> ", set(pred_coarse))

print("gold fine -> ", set(gold_fine))

print("pred fine -> ", set(pred_fine), "\n")

print("Difference in coarse -> ", set(gold_coarse + pred_coarse) - set(fine_to_coarse.values()))
print("Difference in fine -> ", set(gold_fine + pred_fine) - set(fine_to_coarse.keys()))

unknowns = {label for label in gold_fine + pred_fine if label not in fine_to_coarse}
print("Unmapped fine labels:", unknowns, "\n")


from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Coarse labels
#coarse_labels = sorted(set(fine_to_coarse.values()))
coarse_labels = sorted(set(gold_coarse + pred_coarse))
cm_coarse = confusion_matrix(gold_coarse, pred_coarse, labels=coarse_labels)
disp_coarse = ConfusionMatrixDisplay(cm_coarse, display_labels=coarse_labels)
disp_coarse.plot(cmap="Blues")
plt.title("Confusion Matrix - Coarse Types")
#plt.show()
df_cm_coarse = pd.DataFrame(cm_coarse, index=coarse_labels, columns=coarse_labels)
print("Confusion Matrix (Coarse)")
print(df_cm_coarse)

# Fine labels
fine_labels = sorted(set(gold_fine + pred_fine))
cm_fine = confusion_matrix(gold_fine, pred_fine, labels=fine_labels)
disp_fine = ConfusionMatrixDisplay(cm_fine, display_labels=fine_labels)
disp_fine.plot(include_values=False, xticks_rotation=90, cmap="Blues")
plt.title("Confusion Matrix - Fine Types")
plt.tight_layout()
#plt.show()
df_cm_fine = pd.DataFrame(cm_fine, index=fine_labels, columns=fine_labels)
print("Confusion Matrix (Fine)")
print(df_cm_fine)

pd.DataFrame(cm_coarse, index=coarse_labels, columns=coarse_labels).to_csv(conf_course, sep="\t", encoding="utf-8")
pd.DataFrame(cm_fine, index=fine_labels, columns=fine_labels).to_csv(conf_fine, sep="\t", encoding="utf-8")

# Precision recall and f score
from sklearn.metrics import classification_report


def calculate_score(gold, pred, file_n):
    """ """
    
    labels = sorted(set(gold)) 
    report_dict = classification_report(gold, pred, labels=labels, zero_division=0, output_dict=True)
    report_str = classification_report(gold, pred, labels=labels, zero_division=0)
    report_df = pd.DataFrame(report_dict).transpose()
    report_df.to_csv(file_n, sep="\t", float_format="%.4f")
    print(report_str)


calculate_score(gold_coarse, pred_coarse, class_course)

calculate_score(gold_fine, pred_fine, class_fine)

#import json

#def calculate_scores(gold, pred):
#    """ """
#    
##    precision = precision_score(gold, pred)
##    recall = recall_score(gold, pred)
##    f1 = f1_score(gold, pred)

#    precision = precision_score(gold, pred, average='macro')
#    recall = recall_score(gold, pred, average='macro')
#    f1 = f1_score(gold, pred, average='macro')
#    
#    scores = {
#        "precision" : precision,
#        "recall" : recall,
#        "f1" : f1,
##        "precision_mc" : precision_mc,
##        "recall_mc" : recall_mc,
##        "f1_mc" : f1_mc,
#    }
#    
#    return scores


#scores_coarse = calculate_scores(gold_coarse, pred_coarse)
#scores_fine = calculate_scores(gold_fine, pred_fine)

#final_score = {
#    "fine" : scores_fine,
#    "coarse" : scores_coarse
#}

#with open("scores.json", "w") as f:
#    f.write(json.dumps(final_score, ensure_ascii=False))
