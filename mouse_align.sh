#$ -cwd
#$ -S /bin/sh
#$ -j y
#$ -N bwa
#$ -o sysout
#$ -pe thread 2

echo "Running job $JOB_NAME, $JOB_ID on $HOSTNAME"


echo "Aligning to mouse"
#align reads to mouse database
FASTQ1=/directory/to/inputR1.fastq
FASTQ2=/directory/to/inputR2.fastq
BWA=/directory/to/bwa-0.7.12/bwa
INDEX=/directory/to/mouse/index
#names output files and generates output directories for all output files from this script
FN=/directory/to/output/file
AL_SAM="$FN"_mouse.sam
RES="$FN"_bwa_"$JOB_ID"
mkdir -p $RES
#copies the bwa indexed directory (in this cause mouse index) to RES
cp -r /directory/to/mouse/index/mmu $RES/
#app index_file input_file1 input_file2 app_options output_name
time $BWA mem "$RES"/mmus $FASTQ1 $FASTQ2 -t $NSLOTS> $AL_SAM

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
BAC_FASTQ1="$FN"_bac1.fastq
BAC_FASTQ2="$FN"_bac2.fastq
time java -Xmx2g -Djava.io.tmpdir=mytmp -XX:ParallelGCThreads=$NSLOTS -jar $DIR/picard.jar SamToFastq I="$SAM" F="$BAC_FASTQ1" F2="$BAC_FASTQ2"


