import sys
from data import functionKeyList
# a collection of functions for carrying out the semantic analysis


# sends o_stmts block for each function to another function which looks for 
# a) TK_CALL - to see if all calls are to defined functions
# b) TK_BREAK - to see if breaks appear inside while loops
def funcIterator(ASTHead,SymTab,FuncTab, errors):
    numOfScope = len(ASTHead.children)
    for eachfunction in ASTHead.children: 
        for eachstatement in eachfunction.children:
            if eachstatement.val == '<O_stmts>':
                funcChecker(eachstatement,SymTab,FuncTab,numOfScope,errors)
            
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
                print(callparams)
                print(eachparamlist)
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
    
