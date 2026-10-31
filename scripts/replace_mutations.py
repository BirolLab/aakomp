import sys
import re

def parse_mutated_fasta(mutated_fasta_path):
    """
    Manually parses the mutated FASTA and organizes sequences by chromosome and start coordinate.
    Assumes headers look like: >chr1:20528-37628
    """
    mutations = {}
    header_pattern = re.compile(r"^>([^:]+):(\d+)-(\d+)")
    
    current_chrom = None
    current_start = None
    current_end = None
    current_seq_lines = []
    
    def save_record():
        if current_chrom is not None:
            if current_chrom not in mutations:
                mutations[current_chrom] = []
            mutations[current_chrom].append({
                'start': current_start,
                'end': current_end,
                'seq': "".join(current_seq_lines)
            })

    with open(mutated_fasta_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith(">"):
                # Save the previous record before starting a new one
                save_record()
                
                match = header_pattern.search(line)
                if match:
                    current_chrom = match.group(1)
                    current_start = int(match.group(2))
                    current_end = int(match.group(3))
                    current_seq_lines = []
                else:
                    print(f"Warning: Could not parse coordinates from header {line}. Skipping.")
                    current_chrom = None
            else:
                if current_chrom is not None:
                    current_seq_lines.append(line)
                    
    # Catch the final record in the file
    save_record()
        
    # Sort mutations for each chromosome by their start coordinate to ensure left-to-right insertion
    for chrom in mutations:
        mutations[chrom].sort(key=lambda x: x['start'])
        
    return mutations

def write_fasta_sequence(file_handle, sequence, line_length=80):
    """
    Writes a string sequence to a file, wrapping lines at the specified length.
    """
    for i in range(0, len(sequence), line_length):
        file_handle.write(sequence[i:i+line_length] + "\n")

def stream_and_build_genome(original_fasta_path, mutations, output_fasta_path):
    """
    Streams the reference genome one chromosome at a time, applies mutations,
    and writes to the output file to minimize memory usage.
    """
    print(f"Processing genome stream from: {original_fasta_path}")
    
    with open(original_fasta_path, 'r') as ref_file, open(output_fasta_path, 'w') as out_file:
        current_chrom = None
        current_seq_lines = []
        
        def process_chromosome():
            if current_chrom is None:
                return
                
            # Write the new FASTA header
            out_file.write(f">{current_chrom} Mutated via pirs replacement\n")
            original_seq = "".join(current_seq_lines)
            
            if current_chrom not in mutations:
                # No mutations for this chromosome, write it exactly as it was
                write_fasta_sequence(out_file, original_seq)
                return
                
            print(f"Applying mutations to {current_chrom}...")
            new_seq_parts = []
            pointer = 0
            
            for mut in mutations[current_chrom]:
                start = mut['start']
                end = mut['end']
                
                # Append unaltered sequence up to the mutation
                new_seq_parts.append(original_seq[pointer:start])
                # Append the new mutation
                new_seq_parts.append(mut['seq'])
                # Move the pointer to the end of the replaced region
                pointer = end
                
            # Append remaining sequence
            new_seq_parts.append(original_seq[pointer:])
            final_seq = "".join(new_seq_parts)
            
            # Write the newly constructed chromosome
            write_fasta_sequence(out_file, final_seq)

        for line in ref_file:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith(">"):
                # Process and write the previous chromosome before loading the next
                process_chromosome()
                
                # Extract the chromosome ID (e.g., '>chr1' from '>chr1 description...')
                current_chrom = line[1:].split()[0]
                current_seq_lines = []
            else:
                current_seq_lines.append(line)
                
        # Catch the final chromosome in the file
        process_chromosome()
        
    print(f"Finished writing to: {output_fasta_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python replace_mutations_pure.py <original_genome.fa> <mutated_fragments.fa> <output_genome.fa>")
        sys.exit(1)
        
    original_genome_file = sys.argv[1]
    mutated_file = sys.argv[2]
    output_file = sys.argv[3]
    
    mutations_dict = parse_mutated_fasta(mutated_file)
    stream_and_build_genome(original_genome_file, mutations_dict, output_file)