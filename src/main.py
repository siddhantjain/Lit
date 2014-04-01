import sys
import lexicalanalyser
import parser_pda
import parserpart2
import symboltable
from data import regexes

#COMMAND LINE RUN STATEMENT: python src/main.py examples/test2.txt error_lit.txt tokens_lit.txt

#weird way, but this is how main can start
if __name__ == '__main__':
   
    progfilename    =  sys.argv[1]       #TODO: Change all these to command line arguments
    errorfilename   =  sys.argv[2]
    tokfilename     =  sys.argv[3]
    #symtabfilename 	=  "symbol_table.txt"

    
    symboltablelist = []
    lexicalanalyser.lexerControl(tokfilename,errorfilename,progfilename,symboltablelist)

   
    #for each in symboltablelist:
     #   print(each)


    parsetreefile   =  open("parsetree.txt","w+")
    parsetreefile2 = open("parsetree2.txt","w+")
    parsetable = 'ParseTable.csv'
    grammar = 'Grammar.csv'
    #getting the list of tokens generated by lexer
    tokfileR     =  open(tokfilename,"r")
    tokFileString = tokfileR.read()
    listofTokens = tokFileString.split()
    


    rulegenerator = parser_pda.PushDownAutomata(parsetable,grammar,listofTokens)
    generatedrules = rulegenerator.PDAOperation()

    
    if generatedrules[-2] == 'Syntax Error':
        errorfile.write(generatedrules[-1]) 
         
    #Creating the parse Tree
    else:
        RulesDict = parserpart2.createRulesDict(grammar)
        nextrule = parserpart2.RuleNumber(0)
        Head = parserpart2.BuildTree(generatedrules,nextrule,RulesDict)
       

        parserpart2.printtree(Head,parsetreefile)
        parserpart2.printtree2(Head,parsetreefile2,0)
        


