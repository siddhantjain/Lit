import csv
import collections

if __name__ == '__main__':
    
    #progrules = open("examples/programrules.txt","r")
    ruleslistfile = open("src/Grammar_23Mar_Full.csv","r")
    
    RulesDict = defaultdict(list)
    reader = csv.DictReader(ruleslistfile) #create a reader which represents rows in a dictionary form
    for row in reader: #this will read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): #go over each column name and value 
            RulesDict[k].append(v) #append the value into the appropriate list based on column name k
    
    print(RulesDict['Rule Number'])
