#!/bin/bash

REF_GENOME="GCA_009914755.4_T2T-CHM13v2.0_genomic.renamed.fna"

bedtools getfasta \
    -fi "$REF_GENOME" \
    -bed t2t_coding_only.bed \
    -fo T2T-CHM13v2.0_master_coding_only.fa

echo "Extraction done"

