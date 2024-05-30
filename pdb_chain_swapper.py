def swap_and_renumber_pdb(input_pdb, output_pdb):
    with open(input_pdb, 'r') as infile, open(output_pdb, 'w') as outfile:
        lines = infile.readlines()
        
        chain_a_residues = []
        chain_b_residues = []
        
        # Separate residues from chain A and chain B
        for line in lines:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                chain_id = line[21]
                if chain_id == 'A':
                    chain_a_residues.append(line)
                elif chain_id == 'B':
                    chain_b_residues.append(line)
        
        # Renumber residues and atoms, swap chains
        def renumber_and_write_residues(residues, new_chain_id, start_residue_num, start_atom_num):
            current_residue_num = start_residue_num
            current_atom_num = start_atom_num
            previous_residue_id = None
            
            for line in residues:
                residue_id = line[22:26].strip()
                if residue_id != previous_residue_id:
                    current_residue_num += 1
                    previous_residue_id = residue_id
                
                new_line = (line[:6] + f"{current_atom_num:>5}" + line[11:21] + new_chain_id + 
                            f"{current_residue_num:>4}" + line[26:])
                
                outfile.write(new_line)
                current_atom_num += 1
            
            return current_residue_num, current_atom_num
        
        # First write chain B residues as new chain A
        last_residue_num, last_atom_num = renumber_and_write_residues(chain_b_residues, 'A', 0, 1)
        
        # Then write chain A residues as new chain B
        renumber_and_write_residues(chain_a_residues, 'B', last_residue_num, last_atom_num)

# Usage example
input_pdb = 'input_file.pdb'    # Replace with your PDB file name
output_pdb = 'output_file.pdb'  # Name for the output file with swapped and renumbered chains

swap_and_renumber_pdb(input_pdb, output_pdb)
