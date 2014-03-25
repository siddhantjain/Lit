import csv
import re
from collections import defaultdict

class Node(object):
    def __init__(self,val):
        self.val = val
        self.children = []
	

	
    def add_children(self,obj):
        self.children.append(obj)

class RuleNumber(object):
    def __init__(self,val):
        self.val = val


def printtree(obj):
    print("parent is %s and children are: " % obj.val)
    if obj.children:
        for child in obj.children:
            print(" %s " %child.val)
        #print("\n")
        for child in obj.children:
            if child:
                printtree(child)
    else:
        print("None")

def BuildTree(alllines,nextrule,RulesDict):
	#line = progrulefile.next()
    ruleno = alllines[nextrule.val]
    nextrule.val += 1
    nonterm = RulesDict[ruleno][0]
    newnode = Node(nonterm)
    RHS = RulesDict[ruleno][1]
    
    for eachsymbol in RHS.split():
        #print("each symbol %s"%eachsymbol)
        if(re.match("TK_.*",eachsymbol)):				#the symbol is a terminal
            newnode2 = Node(eachsymbol)
            newnode2.children = None
            newnode.children.append(newnode2)
			
        elif(re.match("<.*>",eachsymbol)):				#symbol is a non-terminal
            #progrulefile2 = progrulefile
            nextrule2 = nextrule
            #nextline = progrulefile2.next()
            nextruleno = alllines[nextrule2.val]
            nextnonterm = RulesDict[nextruleno][0]
            matchedsymrule = re.match(nextnonterm,eachsymbol)
            if matchedsymrule:
                newnode3 = BuildTree(alllines,nextrule,RulesDict)
                newnode.children.append(newnode3)
	
    return newnode


def createRulesDict(Grammar):
    ruleslistfile = open(Grammar,"r")
    RulesDict = defaultdict(list)
    reader = csv.DictReader(ruleslistfile,['Rule','LHS','RHS'],delimiter=',') #create a reader which represents rows in a dictionary form
    for row in reader: #this will read a row as {column1: value1, column2: value2,...}
        RulesDict[row['Rule']].append(row['LHS'])
        RulesDict[row['Rule']].append(row['RHS'])
    return RulesDict


    

    




