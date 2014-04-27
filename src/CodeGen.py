import AST
import symboltablefunc
from data import ArithOps

def CodeGenClass(object):
    def __init__(self,ASTHead,SymTab):
        self.ASTHead = ASTHead
        self.SymTab = SymTab
    
    
    def GenerateCode(self):
        codegenfile = open("codegen.txt","w+")
        for eachfunction in self.ASTHead.children:
            self.GenerateFunction(eachfunction,codegenfile)
            
    def GetFreeReg(self):
        for i in range(0,2):
            if AllReg[i][1] == 1:
                AllReg[i][1] = 0
                return AllReg[i][0]
        return None
    
    def DeclareVars(self,ASTDeclStmts,ASTfunc):
        for eachvar in ASTDeclStmts.children:
            freereg = self.GetFreeReg()
            if freereg:
                self.SymTab.symbolTable[self.SymTab.hashfunction(eachvar.children[0].realval,scope)]['register'] = freereg
                self.SymTab.symbolTable[self.SymTab.hashfunction(eachvar.children[0].realval,scope)]['assgnreg'] = bool(1)
    
    
    def AssignStmtCG(self,ASTobjAE,ASTfunc):
        if(ASTobjAE.val == 'TK_ID'):
            return self.SymTab.symbolTable[self.SymTab.hashfunction(ASTobj.realval,scope)]['register']
        elif ASTobjAE.val in ArithOps:
            if(ASTobjAE,children[1].val not in ArithOps) and (ASTobjAE.children[0].val not in ArithOps):
                if()
            
    
    def OStmts(self,ASTOStmts,ASTfunc):
        for eachstmt in ASTOStmts.children:
            if(eachstmt.val == 'TK_ASSIGN'):
                self.AssignStmtCG(eachstmt.children[1],ASTfunc)
                
        
    
    
    def GenerateFunction(self,ASTfunc,codegenfile):
        if(ASTfunc.val == 'TK_MAIN'):
            self.DeclareVars(ASTfunc.children[0],ASTfunc)
            self.OStmts(ASTfunc.children[1],ASTfunc)
            
        
