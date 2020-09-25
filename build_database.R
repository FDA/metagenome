args = commandArgs(trailingOnly=TRUE)
#path to database
db=args[1]
.libPaths('/home/isaac.raplee/R_packages')
library(RSQLite)
require(DBI)
scaffdb <- dbConnect(SQLite(), db)

#-----------------Scaffolds table
dbSendQuery(scaffdb, 'CREATE TABLE Scaffolds (cohortID TINYTEXT,sampID TINYTEXT,
            scaffID TINYTEXT,assn TINYTEXT,length MEDIUMINT UNSIGNED, 
            blastn_cov FLOAT, num_genes SMALLINT UNSIGNED,
            num_mapped_genes SMALLINT UNSIGNED, all_avg_id FLOAT, 
            map_avg_id FLOAT)')

res<-dbSendStatement(scaffdb,'create index SCAFFOLDSIDX1 on Scaffolds (cohortID)')
res<-dbSendStatement(scaffdb,'create index SCAFFOLDSIDX2 on Scaffolds (sampID)')
res<-dbSendStatement(scaffdb,'create index SCAFFOLDSIDX3 on Scaffolds (scaffID)')
res<-dbSendStatement(scaffdb,'create index SCAFFOLDSIDX4 on Scaffolds (assn)')

#-----------------PredictedGenes
dbSendQuery(scaffdb, 'CREATE TABLE PredictedGenes (scaffID TINYTEXT, 
            geneID TINYTEXT, length MEDIUMINT UNSIGNED)')

res<-dbSendStatement(scaffdb,'create index PREDICTEDGENESIDX1 on PredictedGenes (geneID)')
res<-dbSendStatement(scaffdb,'create index PREDICTEDGENESIDX2 on PredictedGenes (scaffID)')

#-----------------PredictedGenes2RefSeq
dbSendQuery(scaffdb, 'CREATE TABLE PredictedGenes2RefSeq (geneID TINYTEXT, 
            sgi TINYTEXT, qstart MEDIUMINT UNSIGNED, qend MEDIUMINT UNSIGNED, 
            sstart MEDIUMINT UNSIGNED, send MEDIUMINT UNSIGNED, evalue FLOAT, 
            bitscore FLOAT, length MEDIUMINT UNSIGNED, ppos FLOAT, pident FLOAT, 
            qcovs FLOAT, prot TEXT, taxid TINYTEXT, org TINYTEXT)')

res<-dbSendStatement(scaffdb,'create index PREDICTEDGENES2REFSEQIDX1 on PredictedGenes2RefSeq (geneID)')
res<-dbSendStatement(scaffdb,'create index PREDICTEDGENES2REFSEQIDX2 on PredictedGenes2RefSeq (taxid)')

#-----------------ScaffLCA
dbSendQuery(scaffdb, 'CREATE TABLE ScaffLCA (scaffID TINYTEXT, 
            superkingdom TINYTEXT, taxid TINYTEXT, sci_name TINYTEXT, 
            tax_rank TINYTEXT)')

res<-dbSendStatement(scaffdb,'create index SCAFFLCAIDX1 on ScaffLCA (scaffID)')
res<-dbSendStatement(scaffdb,'create index SCAFFLCAIDX2 on ScaffLCA (taxid)')


dbDisconnect(scaffdb)
