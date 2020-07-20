#$ -cwd 
#$ -S /bin/sh 
#$ -o sysout
#$ -j y 
#$ -N extract_tax 
#$ -t 1-44

DB_PREFIX=/directory/to/refseq_protein/refseq_protein
DB="$DB_PREFIX"."$SGE_TASK_ID"
if [ $SGE_TASK_ID -lt 10 ]; then
    DB="$DB_PREFIX".0"$SGE_TASK_ID"
fi
export PATH=/directory/to/blast+2.3.0/bin:$PATH
APP=/directory/to/blast+2.3.0/bin/blastdbcmd
RES=/directory/to/blastx/refseq_ac_gi_taxid
mkdir -p $RES
time $APP -db "$DB" -entry "all" -out "$RES"/ref_tax_"$SGE_TASK_ID".txt -outfmt "%a  %g  %T"
 