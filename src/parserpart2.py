import csv
from collections import defaultdict

if __name__ == '__main__':
    
    #progrules = open("examples/programrules.txt","r")
    ruleslistfile = open("src/Grammar_23Mar_Full.csv","r")
    RulesDict = defaultdict(list)
    reader = csv.DictReader(ruleslistfile,['Rule Number','LHS','RHS']) #create a reader which represents rows in a dictionary form
    for row in reader: #this will read a row as {column1: value1, column2: value2,...}
        RulesDict[row['Rule Number']].append('%s42%s'%(row['LHS'],row['RHS']))
    
    print(RulesDict['RULE1'])
