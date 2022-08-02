"""
NCI Gadi Colabfold preprocessing script when predicting the structure 
of numerous protein sequences. This script creates a folder with subfolders 
for each sequence with PBS submission scripts for Colabfold search and 
predict.

This script is unsupported, please contact NCI Help Desk if you have 
issues using Colabfold on Gadi. 

Created by Matt Mortimer https://orcid.org/0000-0002-8135-9319 
matthew.mortimer@anu.edu.au
2022-08-01
"""

import os
from Bio import SeqIO
from datetime import datetime

date_now = datetime.now().strftime('%Y%m%d')
os.mkdir(f"{date_now}_colabfold")

count = 0
parent_dir = f"{date_now}_colabfold/af2_"

project = input("Enter NCI project: ")
user_account = input("Enter NCI user account: ")
walltime_hr = input("Enter walltime in hours: ")
lmem = input("Enter lmem in GB: ")
fasta_file = input("Enter fasta file name: ")

# Read multiple sequence fasta file, one sequence at a time
with open(fasta_file) as sequences:
    for record in SeqIO.parse(sequences, "fasta"):
        count += 1
        # Removes "|" from fasta header, replaces with "-"
        # This will change depend on header format
        if "|" in record.id: 
            record_id = record.id.split("|")
            record_id = "-".join(record_id)
        else:
            record_id = record.id

        # Set unique file number
        file_number = '{:03d}'.format(count)

        # Create iterative path variable
        path = parent_dir + file_number

        # Create unique dir based on path variable, create a results sub-folder
        os.mkdir(path)
        os.mkdir(f"{path}/results")

        # Create single sequence fasta file
        with open(f"{path}/{record_id}.fasta", "w") as f_file:
            SeqIO.write(record, f_file, "fasta")

        # Create search script
        with open(f"{path}/colab_search.sh", "w") as search_script:
            search_script.write(f"#!/bin/bash\n\
\n\
#PBS -P {project}\n\
#PBS -lncpus=12\n\
#PBS -lmem={lmem}GB\n\
#PBS -lwalltime={walltime_hr}:00:00\n\
#PBS -ljobfs=1GB\n\
#PBS -l wd\n\
#PBS -l storage=gdata/if89\n\
\n\
module use /g/data/if89/apps/modulefiles\n\
module load colabfold_batch/1.4.0\n\
\n\
colabfold_search --db-load-mode 1 --threads 12 {record_id}.fasta $COLABFOLDDIR/database /scratch/{project}/{user_account}/{path}/results")

        # Create predict script
        with open(f"{path}/colab_predict.sh", "w") as predict_script:
            predict_script.write(f"#!/bin/bash\n\
\n\
#PBS -P {project}\n\
#PBS -q gpuvolta\n\
#PBS -lncpus=12,ngpus=1\n\
#PBS -lmem={lmem}GB\n\
#PBS -lwalltime={walltime_hr}:00:00\n\
#PBS -ljobfs=1GB\n\
#PBS -l wd\n\
#PBS -l storage=gdata/if89\n\
\n\
module use /g/data/if89/apps/modulefiles\n\
module load colabfold_batch/1.4.0\n\
\n\
colabfold_batch --amber --templates --num-recycle 3 --use-gpu-relax results/0.a3m /scratch/{project}/{user_account}/{path}/results")