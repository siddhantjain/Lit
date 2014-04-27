import AST
import symboltablefunc
from data import ArithOps,AllReg,TokNums,TokVars

class CodeGenClass(object):
    def __init__(self, ASTHead, SymTab, FuncTab):
        self.ASTHead = ASTHead
        self.SymTab = SymTab
        self.FuncTab = FuncTab
        self.ArithOpsDict = {'TK_PLUS':'ADD','TK_MINUS':'SUB','TK_MUL':'MUL','TK_DIV':'DIV'}
        self.BoolOpsDict = {'TK_EQ':'JNE','TK_LTE':'JG','TK_LESS':'JGE','TK_GRTR':'JLE','TK_GTE':'JL','TK_NOTEQ':'JE'}
        self.ifcounter = 1
    
    def GenerateCode(self):
        codegenfile = open("codegen.txt","w+")
        for eachfunction in self.ASTHead.children:
            self.GenerateFunction(eachfunction,codegenfile)
            
    def GetFreeReg(self):
        for i in range(0,7):
            if AllReg[i][1] == 1:
                AllReg[i][1] = 0
                return AllReg[i][0]
        return None
    
    def FreeReg(self,reg):
        for i in range(0,7):
            if (AllReg[i][0] == reg):
                AllReg[i][1] = 1
    
    def DeclareVars(self,ASTDeclStmts,ASTfunc):
        for eachvar in ASTDeclStmts.children:
            freereg = self.GetFreeReg()
            if freereg:
                key = ASTfunc.lineno+ASTfunc.pos
                scope = self.FuncTab[key]['scope']
                self.SymTab.symbolTable[self.SymTab.hashfunction(eachvar.children[0].realval,scope)]['register'] = freereg
                self.SymTab.symbolTable[self.SymTab.hashfunction(eachvar.children[0].realval,scope)]['assgnreg'] = bool(1)
    
    
    def AssignStmtCG(self,ASTobjAE,ASTfunc,codegenfile):
        if(ASTobjAE.val == 'TK_ID'):
            key = ASTfunc.lineno+ASTfunc.pos
            scope = self.FuncTab[key]['scope']
            return self.SymTab.symbolTable[self.SymTab.hashfunction(ASTobjAE.realval,scope)]['register']
        elif ASTobjAE.val in ArithOps:
            if((ASTobjAE.children[1].val not in ArithOps) and (ASTobjAE.children[0].val not in ArithOps)):
                if(ASTobjAE.children[0].val in TokNums):
                    if(ASTobjAE.children[1].val in TokNums):
                        command = 'MOV '
                        freereg = self.GetFreeReg()
                        if freereg:
                            command = command + freereg+','+ASTobjAE.children[1].realval+'\n'
                            print(command)
                            codegenfile.write(command)
                            command = self.ArithOpsDict[ASTobjAE.val] + ' '
                            command += freereg+','+ASTobjAE.children[0].realval+'\n'
                            print(command)
                            codegenfile.write(command)
                            return freereg
            
                    elif(ASTobjAE.children[1].val == 'TK_ID'):
                        command = 'MOV '
                        freereg = self.GetFreeReg()
                        if freereg:
                            command+= freereg+','+ASTobjAE.children[0].realval +'\n'
                            print(command)
                            codegenfile.write(command)
                            command = self.ArithOpsDict[ASTobjAE.val] + ' '
                            key = ASTfunc.lineno+ASTfunc.pos
                            scope = self.FuncTab[key]['scope']
                            varreg = self.SymTab.symbolTable[self.SymTab.hashfunction(ASTobjAE.children[1].realval,scope)]['register']
                            command += freereg+','+varreg+'\n'
                            print(command)
                            codegenfile.write(command)
                            return freereg
            
                elif(ASTobjAE.children[0].val == 'TK_ID'):
                    if(ASTobjAE.children[1].val in TokNums):
                        command = 'MOV '
                        freereg = self.GetFreeReg()
                        if freereg:
                            command = command + freereg+','+ASTobjAE.children[1].realval+'\n'
                            print(command)
                            codegenfile.write(command)
                            command = self.ArithOpsDict[ASTobjAE.val] + ' '
                            key = ASTfunc.lineno+ASTfunc.pos
                            scope = self.FuncTab[key]['scope']
                            varreg = self.SymTab.symbolTable[self.SymTab.hashfunction(ASTobjAE.children[0].realval,scope)]['register']
                            command += freereg+','+varreg+'\n'
                            print(command)
                            codegenfile.write(command)
                            return freereg
                    
                    elif(ASTobjAE.children[1].val == 'TK_ID'):
                        command = 'MOV '
                        freereg = self.GetFreeReg()
                        if freereg:
                            key = ASTfunc.lineno+ASTfunc.pos
                            scope = self.FuncTab[key]['scope']
                            varreg = self.SymTab.symbolTable[self.SymTab.hashfunction(ASTobjAE.children[1].realval,scope)]['register']
                            command+= freereg+','+varreg +'\n'
                            print(command)
                            codegenfile.write(command)
                            command = self.ArithOpsDict[ASTobjAE.val] + ' '
                            key = ASTfunc.lineno+ASTfunc.pos
                            scope = self.FuncTab[key]['scope']
                            varreg = self.SymTab.symbolTable[self.SymTab.hashfunction(ASTobjAE.children[0].realval,scope)]['register']
                            command += freereg+','+varreg+'\n'
                            print(command)
                            codegenfile.write(command)
                            return freereg
    
    
    def OStmts(self,ASTOStmts,ASTfunc,codegenfile):
        for eachstmt in ASTOStmts.children:
            if(eachstmt.val == 'TK_ASSIGN'):
                ansreg = self.AssignStmtCG(eachstmt.children[1],ASTfunc,codegenfile)
                key = ASTfunc.lineno+ASTfunc.pos
                scope = self.FuncTab[key]['scope']
                varreg = self.SymTab.symbolTable[self.SymTab.hashfunction(eachstmt.children[0].realval,scope)]['register']
                command = 'MOV ' + varreg + ',' + ansreg+'\n'
                self.FreeReg(ansreg)
                print(command)
                codegenfile.write(command)
            
            if(eachstmt.val == 'TK_IF'):
                if((eachstmt.children[0].children[0].val in TokVars ) and (eachstmt.children[0].children[1].val in TokVars )):
                    jumpcmd1 = 'CMP '
                    if(eachstmt.children[0].children[0].val == 'TK_ID'):
                        key = ASTfunc.lineno+ASTfunc.pos
                        scope = self.FuncTab[key]['scope']
                        varreg = self.SymTab.symbolTable[self.SymTab.hashfunction(eachstmt.children[0].children[0].realval,scope)]['register']
                        jumpcmd1+= varreg +','
                    else:
                        jumpcmd1+=eachstmt.children[0].children[0].realval+','
                    
                    if(eachstmt.children[0].children[1].val == 'TK_ID'):
                        key = ASTfunc.lineno+ASTfunc.pos
                        scope = self.FuncTab[key]['scope']
                        varreg = self.SymTab.symbolTable[self.SymTab.hashfunction(eachstmt.children[0].children[1].realval,scope)]['register']
                        jumpcmd1+= varreg +'\n'
                    else:
                        jumpcmd1+=eachstmt.children[0].children[1].realval+'\n'
                        
                    print(jumpcmd1)
                    codegenfile.write(jumpcmd1)
                    jumpcmd2 = self.BoolOpsDict[eachstmt.children[0].val] + ' ' + 'if_' + '%d'%self.ifcounter + '\n'
                    
                    print(jumpcmd2)
                    codegenfile.write(jumpcmd2)
                    
                    self.OStmts(eachstmt.children[1],ASTfunc,codegenfile)
                    jumpcmd3 = 'if_'+'%d'%self.ifcounter+':\n'
                    self.ifcounter+=1
                    print(jumpcmd3)
                    codegenfile.write(jumpcmd3)
                    if len(eachstmt.children) >=3:
                        if(eachstmt.children[2].val == 'TK_ELSE'):
                            #print('Reached Here %s '%eachstmt.children[2].children[0].val)
                            self.OStmts(eachstmt.children[2].children[0],ASTfunc,codegenfile)
                        
                    
                    
                    

                
                
        
    
    
    def GenerateFunction(self,ASTfunc,codegenfile):
        if(ASTfunc.val == 'TK_MAIN'):
            self.DeclareVars(ASTfunc.children[0],ASTfunc)
            self.OStmts(ASTfunc.children[1],ASTfunc,codegenfile)
            
        
