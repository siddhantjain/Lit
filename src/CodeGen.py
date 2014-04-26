import AST
import symboltablefunc

def CodeGenClass(object):
    def __init__(self,ASTHead,SymTab):
        self.ASTHead = ASTHead
        self.SymTab = SymTab
    
    
    def GenerateCode(self):
        codegenfile = open("codegen.txt","w+")
        for eachfunction in self.ASTHead.children:
            self.GenerateFunction(eachfunction,codegenfile)
            
    def GetFreeReg(self):
        for i in range(0,3):
            if AllReg[i][1] == 1:
                AllReg[i][1] = 0
                return AllReg[i][0]
        return None
    
    def DeclareVars(self,ASTDeclStmts,ASTfunc):
        for eachvar in ASTDeclStmts.children:
            freereg = self.GetFreeReg()
            if freereg:
                self.SymTab.symbolTable[self.SymTab.hashfunction(eachvar.realval,scope)]['register'] = freereg
                self.SymTab.symbolTable[self.SymTab.hashfunction(eachvar.realval,scope)]['assgnreg'] = bool(1)
    
    def GenerateFunction(self,ASTfunc,codegenfile):
        if(ASTfunc.val == 'TK_MAIN'):
            self.DeclareVars(ASTfunc.children[0],ASTfunc)
            
        
