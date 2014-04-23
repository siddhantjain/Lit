import sys
import lexicalanalyser
import parser_pda
import parserpart2
import symboltablefunc
import AST
import additionalfunctions
from data import regexes

#COMMAND LINE RUN STATEMENT: python src/main.py examples/test2.txt error_lit.txt tokens_lit.txt
#GIT ADD: git add src/main.py src/lexicalanalyser.py src/symboltablefunc.py src/parser_pda.py src/parserpart2.py src/data.py src/AST.py


#weird way, but this is how main can start
if __name__ == '__main__':
   
    progfilename    =  sys.argv[1]       #TODO: Change all these to command line arguments
    errorfilename   =  sys.argv[2]
    tokfilename     =  sys.argv[3]
					
	    
    lexicalanalyser.lexerControl(tokfilename,errorfilename,progfilename)

   
    
    errorfile = open(errorfilename,"w+")
    parsetreefile   =  open("parsetree.txt","w+")
    parsetreefile2 	= open("parsetree2.txt","w+")
    ASTfile = open("ASTfile.txt","w+")
    parsetable = 'ParseTable.csv'
    grammar = 'Grammar.csv'
    #getting the list of tokens generated by lexer
    tokfileR     =  open(tokfilename,"r")
    tokFileString = tokfileR.read()
    listofTokens = tokFileString.split("#")
    #print(listofTokens)


    rulegenerator = parser_pda.PushDownAutomata(parsetable,grammar,listofTokens)
    generatedrules = rulegenerator.PDAOperation()
    
    if generatedrules[-2] == 'Syntax Error':
        errorfile.write(generatedrules[-1]) 
    
    
         
    
    #Creating the parse Tree and symbol table
    else:
        #Instantiating a Symbol Table
        ST = symboltablefunc.symboltableclass()
        RulesDict = parserpart2.createRulesDict(grammar)
        nextrule = parserpart2.RuleNumber(0)
        PTHead = parserpart2.BuildTree(generatedrules,nextrule,RulesDict)
        
        nexttoken = parserpart2.TokenNumber(0)
        parserpart2.TokenInfoinParseTree(listofTokens, PTHead,nexttoken,ST)       #also populates symbol table based on each node

        #print(ST.symbolTable)

        parserpart2.printtree(PTHead,parsetreefile)
        parserpart2.printtree2(PTHead,parsetreefile2,0)
        
        
        #AST Begins
        ASTobj = AST.ASTClass(PTHead)
        ASTobj.ASTHead = ASTobj.BuildAST(ASTobj.ASTHead,PTHead)
        
        ASTobj.PrintAST(ASTobj.ASTHead,ASTfile,0)
        
        
        #Updating Symbol Table
        length = additionalfunctions.retNumOfScope(ASTobj.ASTHead)        
        additionalfunctions.updateScope(ASTobj.ASTHead,ST,length)
        
        #print(ST.symbolTable);       


