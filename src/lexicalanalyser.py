import re
import sys


class Lexeme():							
	#Defines any identified Lexeme in the given string 
	#along with it's token type, value and position. 
    
    def __init__(self, type_, val, pos):				#constructor for intialising
        self.type_ = type_
        self.val = val
        self.pos = pos

    def __str__(self):					 	        #func for printing attributes 						
        return '%s(%s) at %s' % (self.type_, self.val, self.pos) #of the lexeme using print(Lexeme_name)

    
      

class Lexer():
    # The lexer class

       
    def __init__(self, regexes):
        
        #Note to Aki:
        # All the regexes are concatenated into a single regex for easy compilation. 
        # You should read more on groups in MOTW site. 
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

    def input(self, buf):
     #function to initialise the input buffer for the lexer
        self.buf = buf
        self.pos = 0

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
                tok = Lexeme(tok_type, next_unit.group(groupname), self.pos)
                self.pos = next_unit.end()
                return tok

            # if we're here next_unit was not matching any regex
            #TODO: use non-white space regex here
            initial = self.pos                  #stores the initial starting position of error
            while (self.buf[self.pos] != ' '):
                self.pos = self.pos + 1        #finds the end position of erring word (Partially Wrong) 
            tok = Lexeme('TK_ERROR',self.buf[initial:self.pos],initial)
            return tok

    
    def tokens(self):
        # Returns an iterator to the tokens found in the buffer. Iterator is a standard for OOP. You may read up on them
        
        while 1:
            tok = self.token()
            if tok is None: break 
            yield tok

    




