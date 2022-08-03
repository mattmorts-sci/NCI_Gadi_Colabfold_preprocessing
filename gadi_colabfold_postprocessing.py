"""
Place, then run this script in the directory containing the folders with 
each sequence, the submission scripts and colabfold results.

The top ranked relaxed structure from each sequence will be copied to a 
folder called AF2_structures_all and renamed to match the fasta file 
in the original dir.

This script is unsupported.

Created by Matt Mortimer https://orcid.org/0000-0002-8135-9319 
matthew.mortimer@anu.edu.au
2022-08-03
"""

import os
import shutil

# Get and print the current working dir
src_dir = os.getcwd() 
print(src_dir)

# create a dir for the top ranked structures from each sequence
# in all subdirs, pass if dir already exists
dir_name = "AF2_structures_all"

if os.path.exists(dir_name) is False:
    dest_dir = os.mkdir(dir_name)
    os.listdir()
else:
    pass

# Set the directory to copy the structures to
dest_dir = src_dir + "/" + dir_name

# OS walk from bottom up, in each base dir finds the top ranked
# structure and assigns the name to structure. Find the structure
# name based on the name of the fasta file in the same dir. Assigns
# that name to seq_id
for root, dirs, files in os.walk(".", topdown=False):

    for name in files:
        if "0_relaxed_rank_1" in name:
            structure = os.path.join(root, name)
            structure = structure.lstrip("./")
            structure_name = structure.split("/")[-1]

            # Copies the structure to the dest_dir
            shutil.copy(structure, dest_dir)

            # Sets dest_file to the dest_dir + structure file 
            # ie AF2_structures/0_relaxed_rank_1_model_[X].pdb where [X] is variable
            dst_file = os.path.join(dest_dir, structure_name)       

    for name in files:
        if ".fasta" in name:
            seq_id = name.split(".")[0]

            # Assigns the new name to new_dst_file_name
            new_dst_file_name = os.path.join(dest_dir, f"{seq_id}.pdb")

            # Renames the structure
            os.rename(dst_file, new_dst_file_name)

# Changes the working dir and prints list of all files
os.chdir(dest_dir)
dir_lst = os.listdir()
print(f"{len(dir_lst)} structures copied and renamed")
for i in dir_lst:
    print(i)