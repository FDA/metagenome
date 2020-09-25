# Metagenome
## **Project name:** 
 Divergence, lowest common ancestor, and antibiotic resistance profiling pipeline
## **Description:** 
This repository houses every script necessary to run metagenomic NGS data to assess. The figure below provides a nice visual for the pipeline flow. The wiki description provides text explanations of each step.
## **Installation:**
No installation required. Simply download or copy scripts and change all /directory/to/ in the scripts to the appropriate location for your file or software.
## **Steps in order**
1. Remove mouse (host) reads from file with mouse_align.sh against bwa index of mouse genome
2. Assemble reads from mouse_align.sh output into scaffolds/contigs with spades.sh
3. Remove host scaffolds/contigs from output of spades.sh with scaffold_mouse_align.sh
4. Predict genes on scaffolds/contigs from scaffold_mouse_align.sh output with mga.sh
5. Curate output of scaffold_mouse_align.sh into a fasta and txt file of scaffolds/contigs greater than 500bps (500_scaffolds.txt/fasta), a bed and fasta file of predicted genes assigned to the scaffold/contig (pred_genes.bed/fasta), and a txt file containing scaffold coverage details (scaff_coverage.txt).
6a. 500_scaffolds.fasta is mapped to NCBI's non-redundant nt database using blastn.sh and concatenated back together using cat_blastn.py which creates the output blastn_scaff.txt
6b. pred_genes.fasta is mapped to NCBI's non-redundant protein database using run_blastx.sh and concatenated back together using cat_blastx.py which creates the output blastx_genes.txt
6c. cat_contigs.py is ran and uses 500_scaffold.txt + blastx_genes.txt + blastn_scaff.txt to categorize scaffolds/contigs into either known, divergent, or novel creating outputs known_contigs.txt, div_contigs.txt, novel_contigs.txt, cat_contigs_summary.txt, and scaff_class.txt. 
7. pred_genes.fasta is mapped with blastx to NCBI's refseq database using run_refseq_blastx.sh 
8. make_taxonomy_tables.py runs extract_tax.sh and uses output from run_refseq_blastx.sh to create refseq_blastx_genes.txt through a lowest common ancestor taxonomy assignment.
