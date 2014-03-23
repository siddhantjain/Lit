import lexicalanalyser
from data import regexes

#weird way, but this is how main can start
if __name__ == '__main__':
   

    lx = lexicalanalyser.Lexer(regexes)
    progfile = open("program1_lit.txt","r")
    errorfile = open("error_lit.txt","w")
    tokfile = open("tokens_lit.txt","w")
    lineno = 1
    
    for line in progfile:
    	lx.input(line)
    	for tok in lx.tokens():
    	   if tok.type_ == 'TK_ERROR':
    	        errorfile.write ('(%d,%d) \'%s\' doesn\'t follow lexical rules'% (tok.pos,lineno,tok.val))        
    	   else:
    	        tokfile.write ('%s '%tok.type_)
    	lineno+=1
