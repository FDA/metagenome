import string
import os
import sys

mydir=sys.argv[1]
o=str(mydir+'/blastx_genes.txt')
os.chdir(mydir)
num_fasta=0
for name in os.listdir("."):
    if os.path.isdir(name) and "blastx" in name:
        num_fasta+=1
          
reads=dict()
i=1
while i<=num_fasta:
    blastx_folder=str(mydir+'/blastx_'+str(i))
    j=1
    while j<=363:
        blastx_file=str(blastx_folder+'/blastx_'+str(j)+'.txt')
        for x in open(blastx_file):
            for y in x.split('\n'):
                hit=y.split("\t")
                if len(hit[0])!=0:
                    if hit[0] in reads:
                        if float(reads[hit[0]][0])<float(hit[1]):
                            reads[hit[0]]=(hit[1],hit[2],hit[3],hit[4],hit[5],hit[6])
                    else:
                        reads[hit[0]]=(hit[1],hit[2],hit[3],hit[4],hit[5],hit[6])                  
        j+=1
    i+=1

outfile = open(o,'w')
for key, value in reads.items():
    read='\t'.join(reads[key])
    outfile.write("%s\t%s\n" %(key,read))
outfile.close()  

