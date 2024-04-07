for f in Source/non_redundant_fna_split_60000/split_*.fasta; do python 106_extract_defense_sequence_mutiple_inputs.py -i "$f" -g Process/01.PADLOC_find_defense_systems/02.Prepare_defense_list/non_redundant/non_redundant_padloc_withoutDMS.gff -o non_redundant_defense_sequence.fasta; done

