#$ -S /bin/sh
#$ -cwd
#$ -j y
#$ -o sysout
#$ -N python
#$ -l h_vmem=10G
#access python without having to type in "source /projects/mikem/applications/centos/python3/set-run-env.sh
export PATH=/directory/to/python3/bin:$PATH 
export LD_LIBRARY_PATH=/directory/to/python3/lib:$LD_LIBRARY_PATH 
export PYTHONPATH=/directory/to/python3:$PYTHONPATH 
export PYTHONPATH=/directory/to/python3/lib/python3.5:$PYTHONPATH 
export PYTHONPATH=/directory/to/python3/lib/python3.5/site-packages:$PYTHONPATH
#
DIR=/directory/to/sampleLocation/
#
#run python program "get_pred_genes.py" to get high complexity scaffs
#creates pred_genes.bed, scaff_coverage.txt, and 500_scaffolds.txst
time python3 /directory/to/scripts/get_pred_genes.py $DIR
#
#get complex scaffs into fasta starting with the output from mouse scaffold removal process. Gathers all scaffolds greater than 500bps in length
ST_HOME=/directory/to/bin/samtools
time $ST_HOME faidx $DIR/assembled_scaff_sampleName.fasta
time xargs $ST_HOME faidx $DIR/assembled_scaff_sampleName.fasta < $DIR/500_scaffolds.txt >> $DIR/500_scaffolds.fasta
#
#get genes into fasta
BASE=/directory/to/bedtools/bedtools2-2.26.0
APP=$BASE/bin/bedtools
time $APP getfasta -fo $DIR/pred_genes.fasta -fi $DIR/500_scaffolds.fasta -bed $DIR/pred_genes.bed 
