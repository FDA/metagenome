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
