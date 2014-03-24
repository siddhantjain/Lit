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
		self.val = 0


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

def BuildTree(alllines,nextrule):
	
	#line = progrulefile.next()
	line = alllines[nextrule.val]
	nextrule.val+=1
	unit = re.search(r"\s",line)
	#print("flag 1 %s" %line[0:unit.start()])
	ruleno = line[0:unit.start()]
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
			nextline = alllines[nextrule2.val]
			nextunit = re.search(r"\s",nextline)
			#print(nextline[0:unit.start()])
			nextruleno = nextline[0:nextunit.start()]
			nextnonterm = RulesDict[nextruleno][0]
			matchedsymrule = re.match(nextnonterm,eachsymbol)
			if matchedsymrule:
				newnode3 = BuildTree(alllines,nextrule)
				newnode.children.append(newnode3)
	
	return newnode



if __name__ == '__main__':
    
    #progrules = open("examples/programrules.txt","r")
    ruleslistfile = open("Grammar.csv","r")
    RulesDict = defaultdict(list)
    reader = csv.DictReader(ruleslistfile,['Rule Number','LHS','RHS'],delimiter='\t') #create a reader which represents rows in a dictionary form
    for row in reader: #this will read a row as {column1: value1, column2: value2,...}
        #RulesDict[row['Rule Number']].append('%s42%s'%(row['LHS'],row['RHS']))
        RulesDict[row['Rule Number']].append(row['LHS'])
        RulesDict[row['Rule Number']].append(row['RHS'])
    
	#print(RulesDict)
    #parsetreegen("examples/test2rules.txt")
    
    progrulefile = open("examples/test2rules.txt")
    alllines = progrulefile.readlines()
    nextrule = RuleNumber(0)
    Head = BuildTree(alllines,nextrule)
    #Head = BuildTree(progrulefile)
    
    printtree(Head)
    




