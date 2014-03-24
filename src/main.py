import lexicalanalyser
from data import regexes

#weird way, but this is how main can start
if __name__ == '__main__':
   

    lx = lexicalanalyser.Lexer(regexes)
    progfile = open("examples/test1.txt","r")
    errorfile = open("error_lit.txt","w")
    tokfile = open("tokens_lit.txt","w")
    lineno = 1
    counttok = 0
    for line in progfile:
    	lx.input(line)
        alltokens = lx.tokens()
        
    	for tok in alltokens:
    	   if tok.type_ == 'TK_ERROR':
    	        errorfile.write ('(%d,%d) \'%s\' doesn\'t follow lexical rules'% (lineno,tok.pos,tok.val))
           if tok.type_ == 'TK_CMNT':
                continue        
    	   else:
    	        tokfile.write ('%s '%tok.type_)
           
    	lineno+=1
        
