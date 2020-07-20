#$ -cwd 
#$ -S /bin/sh
#$ -l h_rt=96:00:00
#$ -o sysout
#$ -j y 
#$ -N blastx 
#$ -t 1-363

DB_PREFIX=/directory/to/blastx/ncbi_nr_quarterGB/nr
export PATH=/directory/to/blast+2.3.0/bin:$PATH
APP=/directory/to/blast+2.3.0/bin/blastx

DIR=
BLAST_DIR=
RES_DIR=
QUERY=

DB="$DB_PREFIX"_"$SGE_TASK_ID"
time $APP -query $QUERY -db $DB -dbsize 167645032437 -out $RES_DIR/blastx_"$SGE_TASK_ID".txt -outfmt "6 qseqid bitscore pident ppos qcovs evalue sseqid" -max_target_seqs 1 -evalue 1e-6
