# NCI Gadi Colabfold preprocessing for multiple sequences

This repository contains an unsupported script for creating the search and predict scripts for submitting multiple sequences on NCI's Gadi supercomputer. 

## Multisequence protocol:

- You need a fasta file with your sequences (and headers without special characters)
- Create a folder on your desktop, put the fasta file in it
- Place the ‘gadi_colabfold_preprocessing.py’ script in that folder
    - **NB:** Dependencies are Python3 and the Biopython package
    - If you want too change from the Colabfold default settings you will need to edit this script
- Open a terminal window and navigate to the folder, then run:

```bash
python3 gadi_colabfold_preprocessing.py
```

- Follow the prompts and enter:
    - the NCI project ID
    - your NCI user ID
    - The maximum wall time in hours (kept to a minimum)
    - The lmem usage in GB (see Gadi’s PBS script instructions, keep to a minimum)
    - The name of the fasta file
               
- This will create a folder named with [date]_colabfold containing a unique folder for each sequence, with a single sequence fasta file, PBS submission scripts for colabfold search and predict, and a results folder
- Open a terminal and copy the [date]_colabfold folder and contents to your Gadi scratch drive. E.g.

```bash
scp -r Desktop/gadi_colabfold_preprocessing/20220801_colabfold/ mm4134@gadi-dm.nci.org.au:/scratch/ib54/mm4134/
```

- ssh to your Gadi scratch drive and navigate into the copied folder

*Note: it is important you have the copied folder in your user folder ie* /scratch/ib54/mm4134/20220801_colabfold *if it is in another folder or is renamed the PBS submissions scripts will point to the wrong location.*

- Once you are in the copied folder, run the colab_search.sh scripts using a bash script e.g. below, changing the text in square brackets

for i in [standard dir name]{001..[max file number]} ; do (cd "$i" && $echo qsub colab_search.sh) ; done

```bash
for i in 20220802_af2_{001..020} ; do (cd "$i" && $echo qsub colab_search.sh) ; done
```

- When all your jobs have completed, then run the colab_predict.sh scripts using a bash script e.g. below, changing the red text in square brackets

for i in [standard dir name]{001..[max file number]} ; do (cd "$i" && $echo qsub colab_predict.sh) ; done

```bash
for i in 20220802_af2_{001..020} ; do (cd "$i" && $echo qsub colab_predict.sh) ; done
```
