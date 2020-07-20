import string
import os
import sys
tax_rank_names=['superkingdom','kingdom','subkingdom','infrakingdom','parvkingdom','superphylum','phylum','subphylum','infraphylum','parvphylum', 'superclass','class','subclass','infraclass','parvclass','superorder','order','suborder','infraorder','parvorder', 'superfamily','family','subfamily','infrafamily','parvfamily','tribe','subtribe','supergenus','genus','subgenus','infragenus','parvgenus','species group','species','subspecies']

dir=sys.argv[1]

class Gene():
    def __init__(self,line=[]):
        self.name=line[0]
        self.scaff_name=line[0].split(":")[0]
        if line[1] in taxa_info:
            self.taxid_assn=line[1]
            self.lineage=taxa_info[self.taxid_assn].lineage
        else:
            self.taxid_assn="1"
            self.lineage=["1"]
class Scaff():
    def __init__(self,name=""):
        self.name=name
        self.num_genes=0
        self.lineages=[]
        self.lineage=[]
        self.taxid_assn='1'
    def find_lin(self):
        self.lineages.sort(key=lambda item: (-len(item), item))
        longest=self.lineages[0]
        for n,lin in enumerate(self.lineages,1):
            if len(longest)<len(lin):
                lin=lin[:len(longest)]
            matching=True
            last_match='NULL'
            i=0
            #check if whole length of shorter lin matches longer lin
            while i<len(lin):
                if longest[i]!=lin[i]:
                    matching=False
                    break
                elif longest[i] not in tax_rank_names:
                    last_match=i+1
                i+=1
            #if whole length of shorter matches, extend lineage to entire longer lin
            if not matching or i!=len(lin):
                if last_match!='NULL':
                    longest=longest[:last_match]
                #goes to root if superkingdom did not match
                else:
                    longest=["1"]
        self.lineage=longest
        self.taxid_assn=longest[-1]

class Taxid():
    def __init__(self,line=[]):
        self.taxid=line[0]
        self.superkingdom=line[1]
        self.sci_name=line[2]
        self.tax_rank=line[3]
        self.lineage=line[4].split("\t")
        
#loop trough taxa_info.txt to get all the taxon nodes and info
taxa_info=dict()
for x in open('/directory/to/taxonomy/taxa_lin.txt'):
    for y in x.split('\t|\n'):
        line=y.split("\t|\t")
        if len(line[0])!=0:
            taxa_info[line[0]]=Taxid(line)
taxa_info["1"]=Taxid(["1","1","root","root","1"])

top_genes=str(dir+"/top_blastx.txt")
scaffs=dict()
for x in open(top_genes):
    for y in x.split('\n'):
        line=y.split("\t")
        if len(line[0])!=0:
            gene=Gene(line)
            #check if scaff in scaffs already, if not add it
            if gene.scaff_name not in scaffs:
                scaffs[gene.scaff_name]=Scaff(gene.scaff_name)
            scaff=scaffs[gene.scaff_name]
            scaff.num_genes+=1
            if gene.lineage not in scaff.lineages:
                scaff.lineages.append(gene.lineage)
outfile = open(str(dir+'/lca_result.txt'),'w')
for scaff_name, scaff_obj in scaffs.items():
    scaff_obj.find_lin()
    taxa=taxa_info[scaff_obj.taxid_assn]
    outfile.write("%s\t%s\t%s\t%s\t%s\n" % (scaff_obj.name,taxa.superkingdom,taxa.taxid,taxa.sci_name,taxa.tax_rank))
outfile.close()
