import string

class Read():
    def __init__(self,info=0):
        self.info=info
        self.name=0
        self.g=0
        self.n=0
        self.x=0
        self.length=0
    def get_coverage(self):
        coverage=float(self.x)/float(self.g)
        return coverage

samp='sampleName' #Our run through with this file used the sampleName and a fileIdentifier as the base directory for all sample file outputs. 
  #Make sure fn=The location of all of your sample output files of interest.      
fn=str('/'+samp+'fileIdentifier')
#if you did not use a fileIdentifier in addition to the sampleName for your output files you can remove the call to fn in lines of code below and simply use ext.
ext='/directory/to/files'
bed=str(ext+fn+'/500_scaffolds.bed')
bn=str(ext+fn+'/scaff_all.txt')
pred=str(ext+fn+'/pred_genes.bed')
#bx=str(ext+fn+'/genes_all.txt')
bx=str(ext+fn+'/gene_all.txt')
nov=str(ext+fn+'/novel_contigs.bed')
div=str(ext+fn+'/div_contigs.bed')
known=str(ext+fn+'/known_contigs.bed')
scaff_class=str(ext+fn+'/scaff_class.txt')
div_class=str(ext+fn+'/div_class.txt')
known_class=str(ext+fn+'/known_class.txt')
novel_class=str(ext+fn+'/novel_class.txt')
scaffs = [x.rstrip('\n') for x in open(bed)]
blastn = [x.rstrip('\n') for x in open(bn)]
blastx = [x.rstrip('\n') for x in open(bx)]
blastx = [x.replace("::","\t") for x in blastx]
blastx = [x.replace(":","\t") for x in blastx]
genes = [x.rstrip('\n') for x in open(pred)]
reads = dict()
nov_con = []
div_con = []
known_con = []
cons = []
cons1 = []
cons2 = []
cons3 = []
#cons.append('read_name\tlength_bp\tblastn_coverage\tnumber_of_genes\tmean_gene_blastx_ID\tclassification')
#cons1.append('read_name\tlength_bp\tblastn_coverage\tnumber_of_genes\tmean_gene_blastx_ID')
#cons2.append('read_name\tlength_bp\tblastn_coverage\tnumber_of_genes\tmean_gene_blastx_ID')
#cons3.append('read_name\tlength_bp\tblastn_coverage\tnumber_of_genes\tmean_gene_blastx_ID')
i = 0
while i<len(scaffs): 
    read_info=scaffs[i].split("\t")
    #scaff=Read(read_info)
    name=read_info[0].split("_")[1]
    length=read_info[2]
    #info, genes, n coverage, homology, length
    reads[str(name)]=(read_info,int(0),float(0),float(0),int(length))
    #print(reads[str(name)])
    i+=1
j=0
while j<len(blastn):
    hit=blastn[j].split("\t")
    hnum=(hit[0].split("_"))[1]
    if hnum in reads:
        i=reads[str(hnum)][0]
        g=reads[str(hnum)][1]
        n=float(hit[1])
        h=reads[str(hnum)][3]
        l=reads[str(hnum)][4]
        reads[str(hnum)]=(i,g,n,h,l)
    j+=1
j=0
while j<len(genes):
    gene=genes[j].split("\t")
    gnum=(gene[0].split("_"))[1]
    if gnum in reads:
        i=reads[str(gnum)][0]
        g=reads[str(gnum)][1]+1
        n=reads[str(gnum)][2]
        h=reads[str(gnum)][3]
        l=reads[str(gnum)][4]
        reads[str(gnum)]=(i,g,n,h,l)        
    j+=1
j=0
while j<len(blastx):
    xhit=blastx[j].split("\t")
    xnum=(xhit[0].split("_"))[1]
    if xnum in reads:
        i=reads[str(xnum)][0]
        g=reads[str(xnum)][1]
        n=reads[str(xnum)][2]
        h=reads[str(xnum)][3]+float(xhit[5])
        l=reads[str(xnum)][4]
        reads[str(xnum)]=(i,g,n,h,l)
    j+=1

i = 0
while i<len(scaffs): 
    read_info=scaffs[i].split("\t")
    #scaff=Read(read_info)
    name=read_info[0].split("_")[1]
    print(reads[str(name)])
    i+=1
nl=0
dl=0
kl=0
for key, value in reads.items():
    #info, genes, n coverage, homology, length
    read='\t'.join(reads[key][0])
    try:
        cov=float(reads[key][3])/float(reads[key][1])
    except ZeroDivisionError:
        cov=0
    if float(reads[key][2])<=20.0 and cov<=60.0:
        nov_con.append(read)
        read=[]
        read.append(str(reads[key][0][0]))
        read.append(str(reads[key][4]))
        read.append(str(reads[key][2]))
        read.append(str(reads[key][1]))
        read.append(str(cov))
        read='\t'.join(read)
        cons1.append(read)
        nl+=reads[key][4]
    elif float(reads[key][2])>20.0 and float(reads[key][2])<=80.0:
        div_con.append(read)
        read=[]
        read.append(str(reads[key][0][0]))
        read.append(str(reads[key][4]))
        read.append(str(reads[key][2]))
        read.append(str(reads[key][1]))
        read.append(str(cov))
        read='\t'.join(read)
        cons2.append(read)
        dl+=reads[key][4]
    else:
        known_con.append(read)
        read=[]
        read.append(str(reads[key][0][0]))
        read.append(str(reads[key][4]))
        read.append(str(reads[key][2]))
        read.append(str(reads[key][1]))
        read.append(str(cov))
        read='\t'.join(read)
        cons3.append(read)
        kl+=reads[key][4]
print(nl)
print(dl)
print(kl)
      
outfile = open(nov,'w')
for x in nov_con:
    outfile.write("%s\n" % x)

outfile = open(div,'w')
for x in div_con:
    outfile.write("%s\n" % x)

outfile = open(known,'w')
for x in known_con:
    outfile.write("%s\n" % x)
    
outfile = open(scaff_class,'w')
#outfile.write('read_name\tlength_bp\tblastn_coverage\tnumber_of_genes\tmean_gene_blastx_ID\tclassification\n')
file = open(div_class,'w')
for x in cons2:
    outfile.write("%s\t%s\t%s\tdivergent\n" % (cohort,samp,x))
    file.write("%s\n" % x)

file = open(known_class,'w')
for x in cons3:
    outfile.write("%s\t%s\t%s\tknown\n" % (cohort,samp,x))
    file.write("%s\n" % x)

file = open(novel_class,'w')
for x in cons1:
    outfile.write("%s\t%s\t%s\tnovel\n" % (cohort,samp,x))
    file.write("%s\n" % x)
    
    