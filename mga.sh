#$ -S /bin/sh
#$ -cwd
#$ -j y
#$ -o sysout
#$ -N mga

#echo "Running job $JOB_NAME, $JOB_ID on $HOSTNAME"

APP=/directory/to/mga/mga_linux_ia64
#We used an additional location calling to separate cohorts here in original scripts
#which read as MYDIR=//directory/to/working DIR="$MYDIR"/cohort/sampleLocation
MYDIR=/directory/to/sampleLocation
#the output (bacterial scaffolds) from removal of mouse scaffolds
FASTA="$MYDIR"/assembled_scaff_sampleName.fasta

#We used $DIR instead of $MYDIR here in the original scripts to separate into cohorts and sampleLocation
#echo "Sample: $FASTA"
$APP $FASTA -m > $MYDIR/mga_result.txt
#$MYDIR/mga_result.txt was originally #$DIR/mga_result.txt in our working script
mv $MYDIR/sysout/mga.o"$JOB_ID" $MYDIR/mga_result.txt
