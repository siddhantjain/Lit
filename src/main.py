import lexicalanalyser
import parser_pda
import parserpart2

from data import regexes

#weird way, but this is how main can start
if __name__ == '__main__':
   

    lx = lexicalanalyser.Lexer(regexes)

    progfile    =  open("examples/test2.txt","r")       #TODO: Change all these to command line arguments
    errorfile   =  open("error_lit.txt","w")
    tokfile     =  open("tokens_lit.txt","w")
    
    lineno = 1
    for line in progfile:
    	lx.input(line)
        alltokens = lx.tokens()
    	for tok in alltokens:
    	   if tok.type_ == 'TK_ERROR':
    	        errorfile.write ('(%d,%d) \'%s\' doesn\'t follow lexical rules'% (lineno,tok.pos,tok.val))
           elif tok.type_ == 'TK_CMNT':
                continue        
    	   else:
    	        tokfile.write ('%s '%tok.type_)
           
    	lineno+=1
    
    tokfile.close()

    parsetable = 'ParseTable.csv'
    grammar = 'Grammar.csv'
    #getting the list of tokens generated by lexer
    tokfileR     =  open('tokens_lit.txt',"r")
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
       
    #parserpart2.printtree(Head)
