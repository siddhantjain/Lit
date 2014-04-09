import re
import sys
from data import regexes

def lexerControl(tokfilename,errorfilename,progfilename):
    lx = Lexer(regexes)
    progfile    =  open(progfilename,"r")       
    errorfile   =  open(errorfilename,"w")
    tokfile     =  open(tokfilename,"w")
    
    lineno = 1
    for line in progfile:
    	lx.input(line,lineno)
        alltokens = lx.tokens()
    	for tok in alltokens:
    	   if tok.type_ == 'TK_ERROR':
    	        errorfile.write ('(%d,%d) \'%s\' doesn\'t follow lexical rules'% (lineno,tok.pos,tok.val))
           elif tok.type_ == 'TK_CMNT':
                continue        
    	   else:
    	        tokfile.write (str(tok))
    	        
        lineno+=1
    
    tokfile.close()
    #errorfile.close()

class Lexeme():							
	#Defines any identified Lexeme in the given string 
	#along with it's token type, value and position. 
    
    def __init__(self, type_, val, pos,lineno):				#constructor for intialising
        self.type_ = type_
        self.val = val
        self.pos = pos
	self.lineno = lineno

    def __str__(self):					 	        #func for printing attributes 						
        return '~%s~%s~%s~%s~#' % (self.type_, self.val, self.lineno,self.pos) #of the lexeme using print(Lexeme_name)

    
      

class Lexer():
    # The lexer class

       
    def __init__(self, regexes):
        
        # All the regexes are concatenated into a single regex for easy compilation. 
        # We create named groups for each type of regular expression 
        # A name has to be given to each group, which we auto-generate in the following code
        
        count = 1                                                       #just a counter for generation of group names         
        regex_parts = [] 
        self.group_type = {}
	

        for regex, type_ in regexes:
            groupname = 'GROUP%s' % count
            regex_parts.append('(?P<%s>%s)' % (groupname, regex))       #This basically names each group and appends it to the array(list) of regexes 
            self.group_type[groupname] = type_                           #Syntax: (P?<name>pattern)
            count += 1

        self.regex = re.compile('|'.join(regex_parts))                  #a single compilation statement for all Regexes
        self.re_ws_skip = re.compile('\S')                              #a regex to detect a substring with no white spaces    
        self.re_ws = re.compile('\s|\n')                                   #a regex to detect whitespace

    def input(self, buf,bufLineNo):
     #function to initialise the input buffer for the lexer
        self.buf = buf
        self.pos = 0
	self.lineno = bufLineNo

    def token(self):
            # Returns the next lexeme in the form of a Lexeme object(as defined at the beginning)  
            # from the input buffer. 
            # None is returned if the end of the buffer was reached. 
            # In case of a lexing error (the current chunk of the
            # buffer matches no regex), a lexical Error is recorded with
            # the starting position of the error.
        
        if self.pos >= len(self.buf):           #end of buffer reached
            return None
        else:
            
            next_unit = self.re_ws_skip.search(self.buf, self.pos)  #neglects white space and returns next chunk of characters

            if next_unit:
                self.pos = next_unit.start()
            else:
                return None

            next_unit = self.regex.match(self.buf, self.pos)            # checks if the next unit selected is any of the lexeme 
            if next_unit:
                groupname = next_unit.lastgroup
                tok_type = self.group_type[groupname]
                tok = Lexeme(tok_type, next_unit.group(groupname), self.pos,self.lineno)
                self.pos = next_unit.end()
                return tok

            # if we're here next_unit was not matching any regex
            #TODO: use non-white space regex here
            wsmatch=self.re_ws.search(self.buf, self.pos)
            initial = self.pos                  #stores the initial starting position of error
            final = wsmatch.start()
            tok = Lexeme('TK_ERROR',self.buf[initial:final],initial,self.lineno)
            self.pos = wsmatch.end()
            return tok

    
    def tokens(self):
        # Returns an iterator to the tokens found in the buffer. Iterator is a standard for OOP. You may read up on them
        
        tokensperline = []
        tok = self.token()
        while(tok): 
            tokensperline.append(tok)
            tok = self.token()

        return tokensperline
                    
                   
        
            




