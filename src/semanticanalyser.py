import sys
from data import functionKeyList
# a collection of functions for carrying out the semantic analysis


# sends o_stmts block for each function to another function which looks for 
# a) TK_CALL - to see if all calls are to defined functions
# b) TK_BREAK - to see if breaks appear inside while loops
def symbolTableChecker(SymTab,errors):
    for each in SymTab.keyList:
        if (len(SymTab.symbolTable[each]['declared']) > 1):
            errmsg = ("%s defined multiple times in the same scope or it clashes with a globally defined variable"%SymTab.symbolTable[each]['name'])
            errlineno =  SymTab.symbolTable[each]['declared'][0][0]
            errors.append((errmsg,errlineno))
            return errors
            
def funcIterator(ASTHead,SymTab,FuncTab, errors):
    numOfScope = len(ASTHead.children)
    for eachfunction in ASTHead.children: 
        for eachstatement in eachfunction.children:
            if eachstatement.val == '<O_stmts>':
                identifierChecker(eachstatement,SymTab,numOfScope,errors)
                funcChecker(eachstatement,SymTab,FuncTab,numOfScope,errors)
                breakChecker(eachstatement,errors)
        numOfScope-=1

def funcChecker(ASTObj,SymTab,FuncTab,scope,errors):
    if ASTObj.val in ['TK_ASSIGN']:
        lhs = []
        rhs = []  
        funcdefparams = []
        callparams = []
        if ASTObj.children[0].val != '<list_var>':
            lhs.append (ASTObj.children[0])
        else: #in case of a function call being assigned
            for each in ASTObj.children[0].children:
                lhs.append (SymTab.symbolTable[SymTab.hashfunction(each.realval,scope)]['dtype'])
            for each in ASTObj.children[1].children[0].children:
                callparams.append(SymTab.symbolTable[SymTab.hashfunction(each.realval,scope)]['dtype'])
        
            #print(callparams)            
        if ASTObj.children[1].val == 'TK_CALL':
            if ASTObj.children[1].children[0].realval in functionKeyList:
                for functionEntries in functionKeyList[ASTObj.children[1].children[0].realval]:
                
                    rhs.append(FuncTab[functionEntries]['output_parameters'])
                    funcdefparams.append(FuncTab[functionEntries]['input_parameters'])
            else: #if there is no entry for the function in the function table
                errmsg = "definition for function not found"
                errlineno =  ASTObj.children[1].lineno
                errors.append((errmsg,errlineno))
                return errors

            #print(funcdefparams)
            flag1 = 0;
            flag2 = 0;
            
            for eachsignature in rhs:
               if lhs == eachsignature:
                    flag1 = 1;
    
            for eachparamlist in funcdefparams:
                if callparams == eachparamlist:
                    flag2 = 1;     
    
            if flag1 == 0 or flag2 == 0:         
                #print("detected error")
                errmsg = "Function call has no matching function declaration"
                errlineno = ASTObj.children[1].lineno
                errors.append((errmsg,errlineno))
                                    
    elif ASTObj.children:
            for child in ASTObj.children:
                funcChecker(child,SymTab,FuncTab,scope,errors)

#checks if all identifiers are defined and used in scope
def identifierChecker(ASTObj,SymTab,scope,errors):
    gscope = -1 
    if ASTObj.val in ['TK_ID']:
                
        if SymTab.hashfunction(ASTObj.realval,scope) not in SymTab.keyList:
            
            if SymTab.hashfunction(ASTObj.realval,gscope) not in SymTab.keyList: #check for global scope
                errmsg = ("Identifier %s is not defined"%ASTObj.realval)
                errlineno =  ASTObj.lineno
                errors.append((errmsg,errlineno))
                return errors

                if SymTab.symbolTable[SymTab.hashfunction(ASTObj.realval,scope)]['scope'] != scope: 
                    if SymTab.symbolTable[SymTab.hashfunction(ASTObj.realval,scope)]['scope'] != 0:
                        errmsg = ("Identifier %s is not defined in the scope it is being used"%ASTObj.realval)
                        errlineno =  ASTObj.lineno
                        errors.append((errmsg,errlineno))
                        return errors

        
                       
        if SymTab.hashfunction(ASTObj.realval,gscope) in SymTab.keyList: #check if given TK_ID is an array, 
            for child in ASTObj.children:                                #in which case check if indexed id is defined   
                identifierChecker(child,SymTab,scope,errors)
        
        
    elif ASTObj.children:
            for child in ASTObj.children:
                identifierChecker(child,SymTab,scope,errors)

def breakChecker(ASTObj,errors):
    whileranges = []
    #print(ASTObj.val)
    if ASTObj.val in ['TK_BREAK']:
        #print("found breal")
        flag = 0;
        for i in range(len(whileranges)):
            #print (whileranges[i][0])
            #print (whileranges[i][1])
            if ASTObj.lineno > whileranges[i][0] and ASTObj.lineno < whileranges[i+1][0]: 
                flag = 1;
            elif ASTObj.lineno == whileranges[i][0] and ASTObj.lineno > whileranges[i][1] and ASTObj.lineno < whileranges[i+1][0]:
                flag = 1;
            elif ASTObj.lineno > whileranges[i][0] and ASTObj.lineno == whileranges[i+1][0] and ASTObj.lineno < whileranges[i+1][0]:
                flag = 1;
     
        if flag == 0:
           errmsg = ("break statement outside while loop is not allowed")
           errlineno =  ASTObj.lineno
           errors.append((errmsg,errlineno))
           return errors

        if ASTObj.children:
            for child in ASTObj.children:
                breakChecker(child,errors)
   
    elif ASTObj.children:
        for child in ASTObj.children:
            breakChecker(child,errors) 

