import string
import sys
class Scaff():
    def __init__(self,line=""):
        self.name=line
        self.length=float(line.split("_")[3])
        self.genes=[]
        self.cov=0.0
    def get_cov(self):
        end=0.0
        c=0.0
        for gene in self.genes:
            if float(gene.start)<end:
                if float(gene.end)>end:
                    change=float(gene.end)-end
                    c+=change
                    end=float(gene.end)
            else:
                change=float(gene.end)-float(gene.start)
                c+=change
                end=float(gene.end)
        self.cov=(c/self.length)*100

class Gene():
    def __init__(self,line=""):
        self.line=line.split("\t")
        self.start=self.line[1]
        self.end=self.line[2]
        self.strand=self.line[3]
        self.scaff_name=""

dir=sys.argv[1]
print(sys.argv)
mga=str(dir+'/mga_result.txt')
predbed=open(str(dir+'/pred_genes.bed'),'w')
scafftxt=open(str(dir+'/500_scaffolds.txt'),'w')
covtxt=open(str(dir+'/scaff_coverage.txt'),'w')
lines = [x.rstrip('\n') for x in open(mga)]
lines = [x.strip('# ') for x in lines]

i = 0
while i<len(lines):
    if i==0:
        scaff=Scaff(lines[i])
        i+=3        
    elif lines[i][0:5]=='NODE_':
        scaff.get_cov()
        covtxt.write("%s\t%s\t%s\t%s\n" % (scaff.name,str(scaff.length),str(len(scaff.genes)),str(scaff.cov)))
        if scaff.cov>=60 and scaff.length>=500:
            scafftxt.write(str(scaff.name+"\n"))
            for gene in scaff.genes:
                predbed.write("%s\t%s\t%s\t%s\n" % (scaff.name,gene.start,gene.end,gene.strand))
        scaff=Scaff(lines[i])
        i+=3
    else:
        gene=Gene(lines[i])
        gene.scaff_name=scaff.name
        scaff.genes.append(gene)
        i+=1

    
