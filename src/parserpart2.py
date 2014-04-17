import csv
import re
from collections import defaultdict
from data import terminals, nonTerminals

class Node(object):
    def __init__(self,val):
        self.val = val                          #Same as _type. Contains token value
        self.children = []

    def add_children(self,obj):
        self.children.append(obj)
    
    def add_more_details(self,realval,lineno,pos):
        self.realval = realval
        self.lineno = lineno
        self.pos = pos
    
    '''
    def __str__(self, level=0):
        ret = "\t"*level+repr(self.val)+"\n"
        if self.children:
            for child in self.children:
                if child:
                    ret += child.__str__(level+1)
            return ret
    def __repr__(self):
        return "%s" % self.val
    '''
class RuleNumber(object):
    def __init__(self,val):
        self.val = val

class TokenNumber(object):
    def __init__(self,val):
        self.val = val



def printtree2(obj,parsetreefile2, level):
    temp2 = "%s"%obj.val
    
    if obj.val in terminals:
        #if obj.val in ['TK_ID','TK_FUNC','TK_NUM','TK_RNUM','TK_STRLIT']:
        temp2 = "%s %s %s %s"%(obj.val,obj.realval,obj.lineno,obj.pos)
        temp1 ="\t"*level + temp2 + "\n"
        #else:
            #temp1 = "\t"*level + temp2 + "\n"
    else:
        temp1 = "\t"*level + temp2 + ":\n"
    
    parsetreefile2.write(temp1)
    if obj.children:
        for child in obj.children:
            printtree2(child,parsetreefile2, level+1)

        


def printtree(obj,parsetreefile):
    
    parsetreefile.write("\n %s -> " % obj.val)
    if obj.children:
        for child in obj.children:
            parsetreefile.write("%s " %child.val)
        #print("\n")
        for child in obj.children:
            if child:
                printtree(child,parsetreefile)
    else:
        if obj.val in terminals:
            parsetreefile.write("Leaf Node ")
        else:
            parsetreefile.write("NULL")

def BuildTree(alllines,nextrule,RulesDict):
	#line = progrulefile.next()
    ruleno = alllines[nextrule.val]
    nextrule.val += 1
    nonterm = RulesDict[ruleno][0]          #LHS
    newnode = Node(nonterm)
    RHS = RulesDict[ruleno][1]              #RHS
    
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
            nextnonterm = RulesDict[nextruleno][0]      #Check if LHS of next rule is same as this non-terminal
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

def TokenInfoinParseTree(listofTokens,obj,nexttoken,ST):
    #print("Reached HERE 2! %s " %obj.val)
    if obj.val in terminals:
        temp = re.split(r'~',listofTokens[nexttoken.val])                #place of 1 returns the TK_* part of the lexeme
        if temp[1] == obj.val:
            nexttoken.val += 1
            #if obj.val in ['TK_ID','TK_FUNC','TK_NUM','TK_RNUM','TK_STRLIT']:
            obj.add_more_details(temp[2],temp[3],temp[4])
            if obj.val in ['TK_ID','TK_FUNC']:               
                #print('%d'%nexttoken.val)
                if (nexttoken.val < 2):                                 #Note to Sidj-first TK_FUNC declared does not have a previous token
                    prevToken = re.split(r'~',listofTokens[0])[1]
                else:
                    prevToken = re.split(r'~',listofTokens[nexttoken.val -2])[1]            
                ST.addLexeme(obj.val,temp[2],temp[3],temp[4],prevToken)   #Populating Symbol table for the first time
    
    elif obj.children:
        for child in obj.children:
            TokenInfoinParseTree(listofTokens,child,nexttoken,ST)

