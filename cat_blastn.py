import string
import sys
from os import listdir
from os.path import isfile, join

#get directory above /blastn_scaff from command line and to get blastn_dir where the results files are
dir=sys.argv[1]
blastn_dir=str(dir+'/sampleName_blastn_scaff')
#create reads dictionary which will hold the best blastn result for each read
reads=dict()
#find all blastn result files in blastn_dir and put them in a list
blastnfiles = [f for f in listdir(blastn_dir) if isfile(join(blastn_dir, f))]
#this loops over all of the blastn result files
for blastn_file in blastnfiles:
    #remove newline characters from file and turn it into a list bn of lines of the file
    bn = [x.rstrip('\n') for x in open(str(blastn_dir+"/"+blastn_file))]
    #loop over each line in bn
    j=0
    while j<len(bn):
        #split up line bn[j] by the tabs
        hit=bn[j].split("\t")
        #get read name
        name=hit[0].split(":")[0]
        #see if read already exists in the read dictionary
        #if it does exist, edit the result if the new found result has higher coverage
        if name in reads:
            if int(reads[name][0])>int(hit[1]):
                reads[name]=(hit[1],hit[2],hit[3],hit[4])
                #print(name+' '+reads[name][0])
        else:
            reads[name]=(hit[1],hit[2],hit[3],hit[4])
        j+=1

#go through the reads dictionary, join together with tab separators, and write in output
o=str(dir+'/sampleName_blastn_scaff.txt')
outfile = open(o,'w')
for key, value in reads.items():
    read=[]
    read.append(key)
    read.append(reads[key][0])
    read.append(reads[key][1])
    read.append(reads[key][2])
    read.append(reads[key][3])
    read="\t".join(read)
    outfile.write("%s\n" %read)
 
outfile.close()  