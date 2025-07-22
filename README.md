# Evaluation of Samsaadhanii's Compund Analysis

## Instructions:

1. Clone [scl](https://github.com/samsaadhanii/scl.git) and install (includes framing spec.txt, ./configure, make and sudo make install). Keep SCL_CGI=scl, SCL_HTDOCS=scl, TFPATH=/tmp/SKT_TEMP_CPD.
2. Clone [evaluate_scl_cpd](https://github.com/SriramKrishnan8/evaluate_scl_cpd.git) and follow the instructions.
3. Check the working of various SCL tools in the browser.
4. The following should be removed every time make and sudo make install are run. (The exact issue is yet to be checked.)
```
sudo rm -r /tmp/SKT_TEMP_CPD /tmp/CURR_PID_SCL
```
3. Install the following dependencies:
```
pip3 install pandas, numpy, devtrans, tqdm
```

## Evaluation

### Bhagavad Gītā examples

To evaluate the compounds from Bhagavad Gita available in the directory bg_data_start/ and generate the confusion matrix and classification_report:
```
python3 run_compound_analysis_evaluation.py bg_data_start/ bg_res/output.tsv bg_res/error.tsv bg_res/result.tsv bg_res/pairs.tsv

python3 confusion.py bg_res/pairs.tsv bg_res/confusion_matrix_fine.tsv bg_res/confusion_matrix_coarse.tsv bg_res/classification_report_fine.tsv bg_res/classification_report_coarse.tsv
```

### Aṣṣādhyāyī examples

To evaluate the compounds from Ashtadhyayi examples available in the directory asht/ and generate the confusion matrix and classification_report:
```
python3 run_compound_analysis_evaluation_asht_examples.py asht/dev_examples.tsv asht/output.tsv asht/error.tsv asht/result.tsv asht/pairs.tsv

python3 confusion.py asht/pairs.tsv asht/confusion_matrix_fine.tsv asht/confusion_matrix_coarse.tsv asht/classification_report_fine.tsv asht/classification_report_coarse.tsv
```

### Sanskrit Heritage Analysis

To evaluate the performance of SH on Ashtadhyayi avyayībhāva examples
```
python3 sh_cpd_eval.py sh_res avyayIBAva_asht_out.tsv avyayIBAva_asht_out_res.tsv "ab"
```

To evaluate the performance of SH on Ashtadhyayi bahuvrīhi examples
```
python3 sh_cpd_eval.py sh_res avyayIBAva_asht_out.tsv avyayIBAva_asht_out_res.tsv "bv"
```

Similarly for the SHMT examples. The SH output files are given in sh_res/. These are generated from [sandhi_vicchedika](https://github.com/SriramKrishnan8/sandhi_vicchedika.git).
