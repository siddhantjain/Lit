# methods to update the symbol table for furhter checking
import sys
import re

def retNumOfScope(ASTHead):              #takes the number of children of AST head to find the number of scopes
    numOfScope = len(ASTHead.children)
    return numOfScope

#function to update the scope of all 
def updateScope(ASTHead,SymTab,numOfScope):
    for eachfunction in ASTHead.children:
        if(eachfunction.val == 'TK_MAIN' or eachfunction.val == 'TK_FUNC'):
           SymTab.addLexeme(eachfunction.val,eachfunction.realval,eachfunction.lineno,eachfunction.pos,numOfScope,'NULL','NULL')
        for statement in eachfunction.children:
            if statement.val == '<declrtv_stmts>' or statement.val == 'TK_IPP' or statement.val == 'TK_OPP' :
                for declaration in statement.children:
                    if SymTab.symbolTable[SymTab.hashfunction(declaration.children[0].realval)]['scope'] == -1:    #not an array or global variable
                        SymTab.addLexeme(declaration.children[0].val,
                                         declaration.children[0].realval,
                                         declaration.children[0].lineno,
                                         declaration.children[0].pos,
                                         numOfScope, 
                                         declaration.val,
                                         'NULL')
                        


            elif statement.val == '<O_stmts>' or statement.val == 'TK_RET':
                updateReference(statement,SymTab,numOfScope)                 
        numOfScope-=1;
#clear all duplication entries            
    cleanSymTab(SymTab)

#updates the referred field for tokens in the Symbol Table
def updateReference(ASTObj,SymTab,scope):
    if ASTObj.val in ['TK_ID']:
            SymTab.updateLexeme(ASTObj,scope,'referred')
    if ASTObj.children:
            for child in ASTObj.children:
                updateReference(child,SymTab,scope)

  
#to remove duplicate entries in the symbol table
def cleanSymTab(SymTab):
    listkeystoremove = []
    for key in SymTab.keyList:
        if SymTab.symbolTable[key]['scope'] == -1:
           del SymTab.symbolTable[key]
           listkeystoremove.append(key)
          
    for key in listkeystoremove:
        SymTab.keyList.remove(key)
           
             

#function table contains information on function definitions
def updateFunctionTab(ASTHead, FuncTab, FuncKeyList):
    totScope = len(ASTHead.children)
    for eachfunction in ASTHead.children:
        if eachfunction.val == 'TK_FUNC' or eachfunction.val == 'TK_MAIN' :
            inputparamlist = []
            outputparamlist = []
            for parametertype in eachfunction.children:
                if parametertype.val == 'TK_IPP':
                    for parameter in parametertype.children:
                        #store the dtype of the parameter along with its name
                        inputparamlist.append(parameter.val)
                        #print(parameter.val, parameter.children[0].realval)
                        #inputparamlist.append((parameter.val, parameter.children[0].realval))
                
                if parametertype.val == 'TK_OPP':
                    for parameter in parametertype.children:
                        #store the dtype of the parameter along with its name
                        outputparamlist.append(parameter.val)
                        #outputparamlist.append((parameter.val, parameter.children[0].realval))
            #every function is uniquely identifined by the lineno,pos of its declaration
            funckey = eachfunction.lineno + eachfunction.pos
            
            #creating a look up for the keys associated with each function name
            #multiple keys will be associated in case of function overloading
            if eachfunction.realval not in FuncKeyList:
                FuncKeyList[eachfunction.realval] = [funckey]
            else:
                FuncKeyList[eachfunction.realval].append(funckey)
             
            
            
            FuncTablerow = {'funcName': eachfunction.realval,
                            'input_parameters': inputparamlist,
                            'output_parameters': outputparamlist,
                            'scope':totScope }
            #print(FuncTablerow)
            FuncTab[funckey] = FuncTablerow
            totScope -=1
                
            

                                                                     

def findwhileranges(listOfTokens,whileranges):
    for i in xrange(0,len(listOfTokens)):
        if(listOfTokens[i]):
            temp1 = re.split(r'~',listOfTokens[i])[1]
            line1 = re.split(r'~',listOfTokens[i])[3]
            pos1 = re.split(r'~',listOfTokens[i])[4]
            
        else:                                       
            temp1 = '$'
    
        if temp1 == 'TK_WHILE':
            for j in range(i,len(listOfTokens)):
                if(listOfTokens[j]):
                    temp2 = re.split(r'~',listOfTokens[j])[1]
                else:
                    temp2 = '$' 
               

                if temp2 == 'TK_EWHILE':
                    
                    line2 = re.split(r'~',listOfTokens[j])[3]
                    pos2 = re.split(r'~',listOfTokens[j])[4]
    
                    whileranges.append((line1,pos1))
                    whileranges.append((line2,pos2))
                    i=j
                    break

        
                               
    
