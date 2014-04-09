#   Functions for manipulating the symbol table
#   Also contains the Symbol table datastructure
import sys

keyList = []                                            #list of all keys in the symbol table
class symboltableclass:

    def __init__(self):
        self.symbolTable = {}

    def hashfunction(self,name,lineno,pos):                   #calculates key by assuming that the name is in a system with base 62 
        key = 0;        
        for i in range(len(name)):                      # 52 UC and LC alphabest  + 10 digits
            key = key + ord(name[i]) * (62**i)
                                
        return key 

    def addLexeme(self,token,name,lineno,pos,prevToken):
        hashkey = self.hashfunction(name,lineno,pos)
        if(hashkey not in keyList):
            dtype = []
            if token == 'TK_FUNC':
                dtype.append('procname')
                dlist = [(lineno,pos)]
            else:
                print (prevToken)
                if prevToken == 'TK_INT':
                    dtype.append('int')
                elif prevToken == 'TK_FLOAT':
                    dtype.append('float')
                dlist = [(lineno,pos)]
            
            rlist=[]
            symboltableRow =    {'key' : hashkey,
                                'name' : name,
                                'dtype': dtype,
                                'value': 0,
                                'size': 0,
                                'array':bool(0),          #default value. Update it later
                                'scope':0,
                                'declared': dlist,                                          
                                'referred': rlist,
                                'other' : 'NULL'}
            keyList.append(hashkey)
            self.symbolTable[hashkey]=symboltableRow

        else:
            if token == 'TK_FUNC':
                if prevToken == 'TK_CALL':                                               #lexeme when function was called
                    self.symbolTable[hashkey]['referred'].append((lineno,pos))
                else:                                                                   #lexeme in case of function overloading
                    self.symbolTable[hashkey]['declared'].append((lineno,pos))

            elif (prevToken == 'TK_INT' or prevToken == 'TK_FLOAT'):                       #lexeme when same identifier is declared again
                self.symbolTable[hashkey]['declared'].append((lineno,pos))
            else:                                                                       # when identifier is referred
                self.symbolTable[hashkey]['referred'].append((lineno,pos))

                    
