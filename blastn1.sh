#$ -cwd 
#$ -S /bin/sh 
#$ -o sysout
#$ -j y 
#$ -N blastn 
#$ -t 1-136

#In order to run the BLAST+ 2.3.0 database was downloaded locally and split into 1gb pieces
DB_PREFIX=/directory/to/ncbi/nt_split_1G
DB=$DB_PREFIX/nt_"$SGE_TASK_ID"
export PATH=/directory/to/blast+2.3.0/bin:$PATH
APP=/directory/to/blast+2.3.0_fda/bin/blastn

#The 1st argument is the samplefileLocation 
MYDIR=$1
DIR="$MYDIR"/blastn
QUERY="$DIR"/500_scaffolds.fasta

RES_DIR="$DIR"/sampleName_blastn_scaff
mkdir -p $RES_DIR

time $APP -query $QUERY -db $DB -out $RES_DIR/blast_"$SGE_TASK_ID".txt -outfmt "6 qseqid qcovs pident evalue sseqid" -task megablast -evalue 1e-6 -max_target_seqs 1 -best_hit_score_edge 0.05 -best_hit_overhang 0.05 -window_size 0 -perc_identity 90

rm "$MYDIR"/sysout/blastn.o"$JOB_ID"."$SGE_TASK_ID"