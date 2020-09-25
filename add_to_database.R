#-----------------Arguments
args = commandArgs(trailingOnly=TRUE)
#path to working directory with scaff_class.txt, pred_genes.bed, and refseq_blastx_genes.txt data files
db=args[1]
#path to database ex. 
db=args[2]
#name of cohort 
cohort=args[3]
#sample name 
samp=args[4]

setwd(wd)
.libPaths('/directory/to/libs')
library(RSQLite)
require(DBI)
scaffdb <- dbConnect(SQLite(), db)

#------------------------------------Scaffolds table
df<-read.table("scaff_class.txt", sep = '\t',header = F)
dbWriteTable(scaffdb, "Scaffolds", data.frame(cohortID=cohort,sampID=samp,
            scaffID=df$V1, assn=df$V2,length=df$V3,blastn_cov=df$V4,num_genes=df$V5,
            num_mapped_genes=df$V6,all_avg_id=df$V7,map_avg_id=df$V8), append=T)


#------------------------------------PredictedGenes
df<-read.table("pred_genes.bed", sep = '\t',header = F)
df$geneID<- with(df, paste0(V1,":",V2,"-",V3))
df<-transform(df, length = V3-V2+1)
pg<-data.frame(scaffID=df$V1,geneID=df$geneID,length=df$length)
dbWriteTable(scaffdb, "PredictedGenes", data.frame(scaffID=pg$scaffID,geneID=pg$geneID,length=pg$length), append=T)

#------------------------------------PredictedGenes2RefSeq
dbWriteTable(scaffdb, "PredictedGenes2RefSeq", "refseq_blastx_genes.txt",row.names=F, header=F,sep="\t",append=T)

#------------------------------------Get hits for LCA and run get_lca.py
res<-dbGetQuery(scaffdb, '
SELECT geneID, pr.taxid from 
    (SELECT geneID, max(bitscore) mb, min(evalue) me, taxid from 
        (SELECT scaffID, geneID from 
            Scaffolds JOIN PredictedGenes using (scaffID) WHERE Scaffolds.sampID="51_S9") t1
        JOIN PredictedGenes2RefSeq using (geneID) group by geneID) t2
    JOIN PredictedGenes2RefSeq pr using (geneID) where pr.bitscore=mb and pr.evalue=me and pr.ppos>=60 group by geneID
')
write.table(res, "top_blastx.txt",col.names=FALSE,row.names=FALSE,sep="\t",quote=FALSE)

#python code only works in R sometimes... may need to run it before running dbWriteTable with lca_result.txt
system('export PATH=/projects/mikem/applications/centos7/python3/bin:$PATH')
system('export LD_LIBRARY_PATH=/projects/mikem/applications/centos7/python3/lib:$LD_LIBRARY_PATH')
system('export LD_LIBRARY_PATH=/projects/mikem/applications/centos7/python3/usr/lib64:$LD_LIBRARY_PATH')
system('export PYTHONPATH=/projects/mikem/applications/centos7/python3:$PYTHONPATH')
system('export PYTHONPATH=/projects/mikem/applications/centos7/python3/lib/python3.7:$PYTHONPATH')
system('export PYTHONPATH=/projects/mikem/applications/centos7/python3/lib/python3.7/site-packages:$PYTHONPATH')
system(sprintf('python /scratch/isaac.raplee/scripts/get_lca.py %s',wd),wait=TRUE)

#put results from get_lca.py into database
dbWriteTable(scaffdb, "ScaffLCA", "lca_result.txt",row.names=F, header=F,sep="\t",append=T)

dbDisconnect(scaffdb)

quit()
n
         