import sys

script, in_ = sys.argv

in_file = open(in_, 'r')
in_content = in_file.read()
in_file.close()
in_lines = in_content.split('\n')

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

fine_to_coarse = {
    "avyayībhāvaḥ" : "avyayībhāvaḥ",
    "itaretara-dvandvaḥ" : "dvandvaḥ",
    "upapada-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "karmadhārayaḥ" : "tatpuruṣaḥ",
    "kevala-samāsaḥ" : "tatpuruṣaḥ",
    "caturthī-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "tatpuruṣaḥ" : "tatpuruṣaḥ",
    "tṛtīyā-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "dvandvaḥ" : "dvandvaḥ",
    "dvitīyā-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "nañ-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "nañ-bahuvrīhiḥ" : "bahuvrīhiḥ",
    "pañcamī-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "prādi-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "bahuvrīhiḥ" : "bahuvrīhiḥ",
    "ṣaṣṭhī-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "saptamī-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "upamānam" : "tatpuruṣaḥ",
    "dvigu-tatpuruṣaḥ" : "tatpuruṣaḥ",
    "-" : "-",
}

ls_fine = 0
ls_coarse = 0

for line in in_lines:
    
    split_line = line.split('\t')
    
    if split_line[0] == split_line[1]:
        ls_fine += 1
    
    if fine_to_coarse_dev[split_line[0]] == fine_to_coarse_dev[split_line[1]]:
        ls_coarse += 1

print("Fine-grained analysis:")
print(f"Correctly classified: {ls_fine} out of {len(in_lines)}")
print(f"Accuracy: {ls_fine / len(in_lines) * 100:.2f}%")

print("Coarse-grained analysis:")
print(f"Correctly classified: {ls_coarse} out of {len(in_lines)}")
print(f"Accuracy: {ls_coarse / len(in_lines) * 100:.2f}%")
