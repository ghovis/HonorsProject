#! /usr/bin/env python

#  Finds genes in Prokka output annotated from a user defined database, noted by annotation name_db.faa
#  Input csv output from Prokka (.tbl file)
#  Output csv with the start index, stop index, ARG name, Backbone Gene Name, Incompatibility Group, plasmid name
 
import sys
import re
import csv
import copy

def rowsFromProkka(inFile, dbDelim = ".faa"):
	### Note that infile is a .csv file of output from Prokka
    	# Input 
	#	inFile = csv file for reading Prokka output
	# 	dbDelim = the key indicating user defined database in the Prokka output
	# Output
	#	outlist = a list of each CDS's data formatted as
	# 	(start, stop, arg, bg, inc croup, plasmidName, keep (Boolean indicating if it was from a passed in database)
	with open(inFile, "rU") as csvfile:

		csvreader = csv.reader(csvfile, delimiter= '\t')

		#create an empty dictionary to temporarily hold the information for one gene	
		tempout = {"start" : "NA", "stop" : "NA", "geneName" : "NA", "plasmidName" : "NA", 'keep' : False}
		outlist = []

		for line in csvreader: 
			# identify lines specifying the start of a new plasmid
			if len(line) == 1 and line[0].find(">")==0:
				# identify when the plasmids are switching and write out the previous record
				outlist.append([tempout[I] for I in tempout])
				# clear tempout
				tempout = {"start" : "NA", "stop" : "NA", "resName" : "NA", "geneName" : "NA","incGroup" : "NA",\
				 "plasmidName" : line[0][line[0].index(" "):], 'keep' : False}

			# identify rows starting a new CDS
			elif len(line) == 3 and line[2] == 'CDS':
				outlist.append([tempout[I] for I in tempout])
				# replace values in tempout, note that we only need to 
				# replace the plasmid name when we get to a new plasmid
				tempout["start"] = line[0]
				tempout["stop"] = line[1]
				tempout["geneName"] = "NA" 
				tempout["resName"] = "NA" 
				tempout["incGroup"] = "NA" 
				tempout['keep'] = False
		
			# identify if the CDS is from database and tag for keeping
			elif len(line)>4 and line[3] == 'inference' and line[4].find(dbDelim)>-1:
				tempout['keep'] = True
		
			# identify the gene name if it has one
			elif len(line)>4 and line[3] == 'product':
				if "group" not in line[4] and "RES" not in line[4]:
					tempout['geneName'] = line[4]
					tempout['incGroup'] = "NA"
					tempout['resName'] = "NA"
				if "group" in line[4]:
					tempout['incGroup'] = line[4]
					tempout['geneName'] = "NA"
					tempout['resName'] = "NA"
				if "RES" in line[4]:
					tempout['resName'] = line[4]
					tempout['geneName'] = "NA"
					tempout['incGroup'] = "NA"
	return outlist

def cleanList(CDSlist):
	### function removes rows that were not from the current database
	# Input
	#	CDSlist = a list of the information contained for each CDS in one row. 
	#		Last element determines if it was from user defined database
	# Out
	#	returns a list of only the rows from CDS's from our database, 
	#	removes column identifying keeper rows
	return [row[:-1] for row in CDSlist if row[-1]]

print(rowsFromProkka("prokkaAnnotation.tbl"))#insert name of input file (from prokka) here
cleanedUp = (cleanList(rowsFromProkka("prokkaAnnotation.tbl")))#insert name of input file (from prokka) here 


with open('GeneTableOutput.csv','w') as csvfile: #name of output file here
	
	csvwriter = csv.writer(csvfile)
	csvwriter.writerows(cleanedUp)		