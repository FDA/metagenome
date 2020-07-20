#$ -S /bin/sh
#$ -cwd
#$ -j y
#$ -o sysout
#$ -N python
#$ -l h_vmem=50G

BASE=/directory/to/python3
export PATH=$BASE/bin:$PATH
export LD_LIBRARY_PATH=$BASE/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$BASE/usr/lib64:$LD_LIBRARY_PATH
export PYTHONPATH=$BASE:$PYTHONPATH
export PYTHONPATH=$BASE/lib/python3.7:$PYTHONPATH
export PYTHONPATH=$BASE/lib/python3.7/site-packages:$PYTHONPATH

#time python /directory/to/cat_blastx1.py /directory/to/sampleName
#time python /directory/to/cat_blastn.py /directory/to/sampleName
#time python /directory/to/get_pred_genes.py /directory/to/sampleName
time python /directory/to/cat_contigs.py
