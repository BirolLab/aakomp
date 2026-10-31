#!/bin/bash

REF_GENOME="GCA_009914755.4_T2T-CHM13v2.0_genomic.renamed.fna"
PYTHON_SCRIPT="replace_mutations.py"

if [ ! -f "$REF_GENOME" ]; then
    echo "Error: Reference genome $REF_GENOME not found!"
    exit 1
fi

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: Python script $PYTHON_SCRIPT not found!"
    exit 1
fi

for MUTATED_FILE in pirs_mutated_coding_only_*.fa; do
    if [ ! -f "$MUTATED_FILE" ]; then
        continue
    fi

    ID=${MUTATED_FILE#pirs_mutated_}
    ID=${ID%.snp.indel.inversion.fa}
    
    OUTPUT_FILE="T2T_CHM13_${ID}_mutated.fna"
    
    python3 "$PYTHON_SCRIPT" "$REF_GENOME" "$MUTATED_FILE" "$OUTPUT_FILE"
done

echo "Replacement done"

