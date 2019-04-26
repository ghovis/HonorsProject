import re
import csv

with open("/Users/marielelensink/Documents/H2/GeneTable1Edit.csv", 'r') as csvreadfile:
    csvreader = csv.reader(csvreadfile)
    incdict = {}
    outList = []
    incNEW=""
    plasmid = ""
    for line in csvreader:
        plasmid = line[5]
        if not line[4] == 'NA':
            incOLD = line[4]
            if 'Col' in line[4] or 'col' in line[4] or 'Rep' in line[4] or 'rep' in line[4]:
                incNEW = incOLD[5:8] 
            else:
                incNEW = incOLD[5:9]
            incdict[plasmid]=incNEW
    print(incdict)
with open("/Users/marielelensink/Documents/H2/GeneTable1Edit.csv", 'r') as csvreadfile:
    csvreader = csv.reader(csvreadfile)  
    resName1 = ""
    for line in csvreader:
        start= line[0]
        stop = line[1]
        if "RES" in line[2]:
            resName1 = line[2]
            resName = resName1[3:]
        else:
            resName = line[2]
        geneName = line[3]
        plasmid = line[5]
        if plasmid in incdict.keys():
            incgroup = incdict[plasmid]
        else:
            incgroup = "other"  
        outList.append([start,stop,resName,geneName,incgroup,plasmid])
    
with open('GeneTable1.csv','w') as csvwritefile:
    csvwriter = csv.writer(csvwritefile)
    csvwriter.writerows(outList)