#!/usr/bin/env python
from Bio import SeqIO

outFile = "resGenes.faa"
outhandle = open(outFile, 'w')

inSeqs = SeqIO.parse(open("resGenes.fna", "rU"), "fasta")
for record in inSeqs:
	record.seq = record.seq.translate()
	print(record)
	SeqIO.write(record, outhandle, "fasta")
outhandle.close()
	
	
		
