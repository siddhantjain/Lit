# methods to update the symbol table for furhter checking
import sys

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

def cleanSymTab(SymTab):
    for key in SymTab.keyList:
        if SymTab.symbolTable[key]['scope'] == -1:
            del SymTab.symbolTable[key]


#remove duplicate entries which were made in the symbol table
#def cleanSymTab(SymTab):

                                                                     
