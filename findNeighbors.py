import csv
with open("/Users/marielelensink/Documents/H2/GeneTable2000.csv",'r') as  csvreadfile:
    csvreader = csv.reader(csvreadfile)
    tempN1 = ""
    N1 = ""
    N2 = ""
    outList = []
    resList = []
    afterRES = False 
    for line in csvreader:
        if not line[3] == "NA" and afterRES == False:
            tempN1 = line[3]
        if not line[2] == "NA":
            N1 = tempN1
            resName = line[2]
            afterRES = True 
            resList.append(resName)
        if not line[3] == "NA" and afterRES == True:
            N2 = line[3]
            afterRES = False
            for gene in resList:
                outList.append([gene,N1,N2,line[4],line[5]])
            tempN1 = line[3]
            resList = []
    print(outList)
with open('neighbors2000.csv','w') as csvwritefile:
    csvwriter = csv.writer(csvwritefile)
    csvwriter.writerows(outList)