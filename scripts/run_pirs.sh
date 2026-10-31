#!/bin/bash

coding_input="T2T-CHM13v2.0_master_coding_only.fa"

snv_rates=(0.010 0.020 0.030 0.040 0.050)
indel_rates=(0.0010 0.0020 0.0030 0.0040 0.0050)
display_p=(1.1 2.2 3.3 4.4 5.5)

for i in {0..5}; do
    v_rate="${snv_rates[$i]}"
    d_rate="${indel_rates[$i]}"
    pct="${display_p[$i]}"
    
    out_prefix="pirs_mutated_coding_only_snv_${pct}"
    final_output="T2T-CHM13v2.0_mutated_coding_only_snv_${pct}pct.fa"
    
    pirs diploid \
        "$coding_input" \
        -s "$v_rate" \
        -d "$d_rate" \
        -o "$out_prefix" \
        -S 42
    
    if [ -f "${out_prefix}.snp.indel.cnv.fa.1" ]; then
        sed 's/_[12]$//' "${out_prefix}.snp.indel.cnv.fa.1" > "$final_output"
        rm -f "${out_prefix}.snp.indel.cnv.fa.1" \
              "${out_prefix}.snp.indel.cnv.fa.2" \
              "${out_prefix}"*.txt \
              "${out_prefix}"*.vcf
    fi
done

echo "pIRS done"

