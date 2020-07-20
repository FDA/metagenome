#$ -cwd
#$ -l h_vmem=150G
#$ -S /bin/sh
#$ -o sysout
#$ -j y
#$ -N metaspades
#$ -pe thread 8


echo "Running job $JOB_NAME ($JOB_ID) on $HOSTNAME"
export PATH=/directory/to/SPAdes-3.12.0-Linux/bin:$PATH
APP=/directory/to/SPAdes-3.12.0-Linux/bin/spades.py
#location of were you would like to work from. This is where we placed all of our samples.
MYDIR=/directory/to/working
#location of samples files. If following along in pipeline this would be the output directory from mousealign.sh output.
FN="$MYDIR"/samplefileDirectory

#Files of interest. If following the pipeline presented these would be the output files from the mosuealign.sh
FASTQ1="$FN"_bac1.fastq
FASTQ2="$FN"_bac2.fastq
#The directory you would like SPAdes to place output files.
RES="$FN"_spades
mkdir -p $RES 

echo "Running metaspades"
#you can use the --continue -o "outputdirectory" to resume from last available checkpoint. If you need to start from a specific checkpoint use --restart-from <chechpoint>
#you can turn off gzip output with --disable-gzip-output
#if auto detect phred fail you can set phred to 33 or 64 (33 for newer cleaner data)
time python $APP -k 21,33,55,77 --meta -1 $FASTQ1 -2 $FASTQ2 -t $NSLOTS --memory 150 --phred-offset 33 -o $RES
