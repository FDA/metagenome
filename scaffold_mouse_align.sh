#$ -cwd
#$ -S /bin/sh
#$ -j y
#$ -N bwa
#$ -o sysout
#$ -pe thread 2

echo "Running job $JOB_NAME, $JOB_ID on $HOSTNAME"


echo "Aligning to mouse"
#align reads to mouse database
FASTQ1=/directory/to/SPAdes/output/scaffolds.fasta
BWA=/directory/to/bwa-0.7.12/bwa
#directory to BWA indices
INDEX=/directory/to/mmus
#names output files and generates output directories for all output files from this script
FN=/directory/to/output/sampleName
AL_SAM="$FN"_mouse.sam
#app index_file input_file1 input_file2 app_options output_name
time $BWA mem $INDEX $FASTQ1 -t $NSLOTS> $AL_SAM

echo "extracting unmapped reads"
#extract umapped reads and convert to .sam
ST_HOME=/directory/to/samtools
SAM="$FN"_bac.sam
time $ST_HOME view -h -f 4 $AL_SAM > $SAM

echo "converting to fastq"
#convert to fastq
export JAVA_HOME=/directory/to/java/jre1.8.0_91
export PATH=/directory/to/java/jre1.8.0_91/bin:$PATH
export LD_LIBRARY_PATH=/directory/to/picard/picard-tools-2.1.1:$LD_LIBRARY_PATH
DIR=/directory/to/picard/picard-tools-2.1.1
BAC_FASTQ1="$FN"_bac.fastq
time java -Xmx2g -Djava.io.tmpdir=mytmp -XX:ParallelGCThreads=$NSLOTS -jar $DIR/picard.jar SamToFastq I="$SAM" F="$BAC_FASTQ1"


