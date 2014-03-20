import lexicalanalyser
from data import regexes
if __name__ == '__main__':
   

    lx = lexicalanalyser.Lexer(regexes)
    inputstring = '_functionName int a; $a <- $b+$c'
    lx.input(inputstring)
    
    
    
    for tok in lx.tokens():
        test = tok.type_
        if tok.type_ == 'TK_ERROR':
            print ('PRINT IN ERROR FILE:    %s'%tok.__str__())        
        else:
            print(tok)
