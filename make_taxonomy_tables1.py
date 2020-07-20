"""
refseq gis to taxid were obtained by running blastdbcmd on the refseq database -outfmt "%g  %T"
download files gi_taxid_prot.dmp.gz and taxdump.tar.gz from website
ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/
Linux commands:
gunzip gi_taxid_prot.dmp.gz
tar -xvzf taxdump.tar.gz
cd /to/directory/with/these/files
"""

#Taxid class initiated with split line from nodes.dmp, called to create for each new taxid
class Taxid():
    def __init__(self,line=''):
        self.taxid=line[0]
        self.parent_taxid=line[1]
        self.rank=line[2]
        self.sci_name=""

#a dictionary that we will use to quickly access info
taxids=dict()
#populate dict with taxids, parents, and taxonomy rank
for x in open('nodes.dmp'):
    for y in x.split('\t|\n'):
        line=y.split("\t|\t")
        if line[0]!='':
            tax_ob=Taxid(line)
            taxids[tax_ob.taxid]=tax_ob
print("read in nodes.dmp")

#get scientific names
for x in open('names.dmp'):
    for y in x.split('\t|\n'):
        line=y.split("\t|\t")
        if line[0]!='':        
            if line[3]=="scientific name":
                taxids[line[0]].sci_name=line[1]
print("read in names.dmp")

#make table with columns taxid, parent_taxid, rank, scientific name
taxa_info = open('taxa_info.txt','w')
for key,value in taxids.items():
    taxa_info.write("%s\t%s\t%s\t%s\n" % (value.taxid,value.parent_taxid,value.rank,value.sci_name))
taxa_info.close()
print("created taxa_info.txt")

#get refseq gis only
#make table with columns gi, taxid, parent_taxid, rank, scientific name
ref_gi2taxa=open('refseq_gi2taxa.txt','w')
i=1
while i<=44:
    ref_gi_file=str('/directory/to/blastx/refseq_ac_gi_taxid/ref_tax_'+str(i)+'.txt')
    for x in open(ref_gi_file):
        for y in x.split('\n'):
            line=y.split("  ")
            if line[0]!='':
                gi=line[1]
                try:
                    tax_ob=taxids[line[2]]
                    ref_gi2taxa.write("%s\t%s\t%s\t%s\t%s\n" % (gi,tax_ob.taxid,tax_ob.parent_taxid,tax_ob.rank,tax_ob.sci_name)) 
                except KeyError:
                    pass                
    i+=1
ref_gi2taxa.close()
print("created refseq_gi2taxa.txt")
tax_rank_names=['superkingdom','kingdom','subkingdom','infrakingdom','parvkingdom','superphylum','phylum','subphylum','infraphylum','parvphylum', 'superclass','class','subclass','infraclass','parvclass','superorder','order','suborder','infraorder','parvorder', 'superfamily','family','subfamily','infrafamily','parvfamily','tribe','subtribe','supergenus','genus','subgenus','infragenus','parvgenus','species group','species','subspecies']
class Taxid():
    def __init__(self,line=[]):
        self.taxid=line[0]
        self.parent_taxid=line[1]
        self.tax_rank=line[2]
        if self.tax_rank not in tax_rank_names:
            self.tax_rank="no rank"
        self.sci_name=line[3]
        self.full_lineage=[]
        self.superkingdom=""
#loop trough taxa_info.txt to get all the taxon nodes and info
taxa_info=dict()
for x in open('/directory/to/taxonomy/taxa_info.txt'):
    for y in x.split('\n'):
        line=y.split("\t")
        if len(line[0])!=0:
            taxa_info[line[0]]=Taxid(line)

#get linages for each taxon node
outfile = open('/directory/to/taxonomy/taxa_lin.txt','w')
for taxid,tax_obj in taxa_info.items():   
    lfull=[]
    lfull.append(taxid)
    #crawl up through parent nodes and at superkingdom
    parent_obj=taxa_info[tax_obj.parent_taxid]
    while parent_obj.taxid!="1":
        lfull.append(parent_obj.taxid)
        if parent_obj.tax_rank=="superkingdom":
            break
        parent_obj=taxa_info[parent_obj.parent_taxid]
    #flip list so starts at superkingdom
    lfull=list(reversed(lfull))
    #this is to put the taxids in relation to the named taxonomic ranks, ei even if taxon node is listed as no rank
    i1=0
    i2=0
    known_rank="no rank"
    #go to subspecies
    while i2<len(lfull) and i1<len(tax_rank_names):
        t=lfull[i2]
        if taxa_info[t].tax_rank=="superkingdom":
            tax_obj.superkingdom=t
        #if the taxid has a listed taxon rank, substitute it for the rank name move forward in taxon rank names and the taxid lineage
        if tax_rank_names[i1]==taxa_info[t].tax_rank:
            tax_obj.full_lineage.append(t)
            #keep the latest name taxon rank
            known_rank=tax_rank_names[i1]
            i1+=1
            i2+=1
        #else if the taxid does not have a rank, add it and only move forward in the taxid lineage
        elif taxa_info[t].tax_rank not in tax_rank_names:
            tax_obj.full_lineage.append(t)
            i2+=1   
        #if the taxid does have a rank but it is not at the correct place in the taxon rank names, add the in between rank name
        else:
            tax_obj.full_lineage.append(tax_rank_names[i1])
            i1+=1
    #if the lineage has taxids below the subspecies level, add them
    while i2<len(lfull):
        t=lfull[i2]
        tax_obj.full_lineage.append(t)
        i2+=1      
    if tax_obj.tax_rank=="no rank":
        tax_obj.tax_rank=known_rank
    ol="\t".join(tax_obj.full_lineage)
    outfile.write("%s\t|\t%s\t|\t%s\t|\t%s\t|\t%s\t|\n" % (tax_obj.taxid,tax_obj.superkingdom,tax_obj.sci_name,tax_obj.tax_rank,ol))
