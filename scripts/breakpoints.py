import argparse
import random
from collections import defaultdict

def read_fasta(fasta_file):
    sequences = []
    current_seq = []
    
    with open(fasta_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_seq:
                    sequences.append("".join(current_seq))
                    current_seq = []
            else:
                current_seq.append(line)
                
        if current_seq:
            sequences.append("".join(current_seq))
            
    return sequences

def get_total_coordinates(sequences):
    total_coordinates = []
    for idx, seq in enumerate(sequences):
        for pos in range(1, len(seq)):
            total_coordinates.append((idx, pos))
            
    return total_coordinates

def introduce_breakpoints(sequences, breakpoints):
    breaks_map = defaultdict(list)
    for idx, pos in breakpoints:
        breaks_map[idx].append(pos)
    
    fragments = []
    for i, seq in enumerate(sequences):
        cuts = sorted(breaks_map[i])
        
        start = 0
        for c in cuts:
            fragments.append(seq[start:c])
            start = c
        
        fragments.append(seq[start:])

    return fragments

def main():
    parser = argparse.ArgumentParser(description="Make breakpoints.")
    parser.add_argument("fasta_file", help="Path to input FASTA")
    parser.add_argument("n", type=int, help="Number of breakpoints")
    args = parser.parse_args()

    seqs = read_fasta(args.fasta_file)
    coords = get_total_coordinates(seqs)


    selected = random.sample(coords, args.n)
    fragments = introduce_breakpoints(seqs, selected)

    for i, frag in enumerate(fragments, 1):
        print(f">Fragment_{i}\n{frag}")

if __name__ == "__main__":
    main()

