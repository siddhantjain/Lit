#   Functions for manipulating the symbol table
#   Also contains the Symbol table datastructure
import sys

                                           #list of all keys in the symbol table
class symboltableclass:

    def __init__(self):
        self.symbolTable = {}
        self.keyList = []

    def hashfunction(self,name,scope=-1):                   #calculates key by assuming that the name is in a system with base 62 
        key = 0;        
        for i in range(len(name)):                      # 52 UC and LC alphabest  + 10 digits
            key = key + ord(name[i]) * (62**i)
            key =  key+ int(scope)                            #There can be only one unique id in given scope                    
        return key 

    def addLexeme(self,token,name,lineno,pos,scope = -1,prevToken='NULL',followingToken='NULL'):
        hashkey = self.hashfunction(name,scope)
        
        if(hashkey not in self.keyList):
            dtype = []
            rlist = []
            dlist = []
            array = bool(0)
            
            if token == 'TK_FUNC':
                dtype = 'procname'
                if prevToken == 'TK_END' or prevToken == 'NULL':
                    dlist = [(lineno,pos)]
                    scope = 0;
                elif prevToken == 'TK_CALL':
                    rlist.append((lineno,pos)) 
                    
                    
            else:
                #print (prevToken)
                if prevToken == 'TK_INT':
                    dtype = 'TK_INT'
                    #dtype.append('TK_INT')
                    dlist = [(lineno,pos)]
                elif prevToken == 'TK_FLOAT':
                    dtype = 'TK_FLOAT'                    
                    #dtype.append('TK_FLOAT')
                    dlist = [(lineno,pos)]
                else:
                    rlist.append((lineno,pos))

                if followingToken == 'TK_OSQ':
                    array = bool(1)
                    scope = 0                                   #note: arrays are global by default
                if followingToken == 'TK_GLOBAL':                           
                    scope = 0
                
            
            
            symboltableRow =    {'name' : name,
                                'dtype': dtype,
                                'value': 0,
                                'size': 0,
                                'array':array,          #default value. Update it later
                                'scope':scope,
                                'declared': dlist,                                          
                                'referred': rlist,
                                'assgnreg': bool(0),
                                'address': 'NULL',
                                'register': 'NULL'}
            self.keyList.append(hashkey)
            self.symbolTable[hashkey]=symboltableRow

        else:

            if token == 'TK_FUNC':
                if prevToken == 'TK_CALL':                   #lexeme when function was called
                                                                  
                    self.symbolTable[hashkey]['referred'].append((lineno,pos))
                else:                                                                   #lexeme in case of function overloading
                    #print(prevToken);
                    self.symbolTable[hashkey]['declared'].append((lineno,pos))          # can be used to index in functable in case of Func. OverL.

            elif (prevToken == 'TK_INT' or prevToken == 'TK_FLOAT'):                       #lexeme when same identifier is declared again
                self.symbolTable[hashkey]['declared'].append((lineno,pos))
            else:                                                                       # when identifier is referred
                self.symbolTable[hashkey]['referred'].append((lineno,pos))


        #function to change one attribute value of an existing entry    
    def updateLexeme(self,ASTObj,scope,attribute):    
        if(self.hashfunction(ASTObj.realval,scope) in self.keyList):
            if attribute == 'referred': #add the line,pos where the variable was referred
                self.symbolTable[self.hashfunction(ASTObj.realval,scope)][attribute].append((ASTObj.lineno,ASTObj.pos))
            #add other conditions based on the attribute entered

    

             
'''  
        elif(self.hashfunction(ASTObj.realval) in keylist):                               #case when variable is in symtab but scope not updated
            tempsymtablerow = symbolTable[self.hashfunction(ASTObj.realval)]
            if (len(tempsymtablerow['declared']) > 1 ):                         #case when same variable has been declared in mul functions
                tempsymtablerow['declared'] = [(ASTObj.lineno,ASTObj.pos)]
                symbolTable[self.hashfunction(ASTObj.realval).remove([(ASTObj.lineno,ASTObj.pos)])]
            tempsymtablerow['scope'] = scope
            tempsymtablerow['key']=self.hashfunction(name,scope)
            
            
            return 0                                            #key not found. Return 0
       
'''
