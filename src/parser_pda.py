# An implementation for push-down automata to generate the list of rules for deriving the given rules
# Generates an error if the input string can't be derived
# grammar is available in grammar.csv
# parse table has been created already and available in parsetable.csv
# data.py has list of terminals and non-terminals

import sys
import csv
import shlex
import re
from data import terminals,nonTerminals

class Stack:
     def __init__(self):
         self.container = []  

     def isEmpty(self):
         return self.size() == 0    

     def push(self, item):
         self.container.append(item)  

     def pop(self,flag=1):                                        #pos = 0 => pop from top. 
        if flag:
           return self.container.pop()                         #Default: pop from end of stack
           
        else:
            return self.container.pop(0)
            #print ("reading from the end")

     def head(self,flag=1):
        if flag:        
            return self.container[-1]
            
        else:
            return self.container[0]
            
     def size(self):
         return len(self.container)  # length of the container

class PushDownAutomata():
    
    def __init__(self,parsetable,grammar,listofTokens):     #pass name of parsetable file as parameter
        self.PDAStack = Stack()
        self.inputTokStack = Stack()
        self.PDAAction = []
        self.listofTokens = listofTokens
        #PTDict is the parse table dictionary for the PDA         
        self.PTDict = csv.DictReader(open(parsetable, 'rb'), delimiter=',')
        self.GramDict = csv.DictReader(open(grammar,'rb'), delimiter = ',')
        #initialisation operations        
        self.PDAStack.push('$')
        self.PDAStack.push('<Program>')
        
        
    def createParseTableMetaDict(self,PTDict):              #creates a dictionary of the rows in the parsetable dictionary
        result = {}
        for row in PTDict:
            key = row.pop('NonTerminals')
            result[key] = row
        return result
  
    def createGrammarMetaDict(self,gramDict):              #creates a dictionary of the rows in the parsetable dictionary
        result = {}
        for row in gramDict:
            key = row.pop('Rule')
            result[key] = row
        return result

    def getToken(self,word,place):                                #returns attribute from the lexeme based on place
        if(word):
            temp = re.split(r'~',word)[place]
            #print(temp)                     #example: returns TK_MAIN from word = ~TK_MAIN~_main~2~0~ and pos = 1
            return temp
        else:                                       #returns $ if word is NULL
            return '$'                              #in given stream of tokens and so we don;t need to push a $ seperately in the stack 
    

    def PDAOperation(self):
    #beginning PDA operation
    #initialising input token stack
         
         for word in self.listofTokens:
             self.inputTokStack.push(self.getToken(word,1))
         
         #self.inputTokStack.push('$')

         parsetable = self.createParseTableMetaDict(self.PTDict)
         grammar = self.createGrammarMetaDict(self.GramDict)
         topOfStack = self.PDAStack.pop()
         topOfInput = self.inputTokStack.head(0)      #Just check what is there on the Top!
         
       

         while(topOfStack != '$'):
            if topOfStack in nonTerminals:                                          # if topOfStack is a nonTerminal    
                nextRule = parsetable[topOfStack][topOfInput]
                if nextRule == '':              #check this condition
                    #print ('Syntax Error: No matching rule for derivation')
                    self.PDAAction.append('Syntax Error')
                    self.PDAAction.append('\nSyntax Error: No matching rule for derivation')
                    return self.PDAAction
                else:
                    nextRule = 'RULE%s'%nextRule
                    #print(nextRule)
                    self.PDAAction.append(nextRule)
                    toPush = grammar[nextRule]['RHS'].split()                  #need to reverse for correct order of pushing
                    toPush= reversed(toPush)
                    # print(toPush)
                    for temp in toPush:
                        if temp != 'NULL':
                            self.PDAStack.push(temp)

                            #print(temp)
           
            elif topOfStack in terminals:                                   # if topOfStack is a terminal
                if (topOfStack == self.inputTokStack.head(0)):              # Check if input token stream also has the same terminal as head
                    self.inputTokStack.pop(0)                   
                    topOfInput = self.inputTokStack.head(0)
                   
                else:
                    #print ('Syntax error: Terminals do not match')
                    self.PDAAction.append('Syntax Error')                                          # else this is a syntax error
                    self.PDAAction.append('\nSyntax Error: Terminals do not match') 
                    return self.PDAAction       
       
            topOfStack = self.PDAStack.pop()                                         #Getting next top of Stack    
            
        #if we are here we have reach $ the stack
            
         if(self.inputTokStack.head(0) == '$'):
            return self.PDAAction
         else:
            self.PDAAction.append('Syntax Error')
            self.PDAAction.append('\nSyntax Error: some input tokens could not be derived')
            return self.PDAAction
                    
    
