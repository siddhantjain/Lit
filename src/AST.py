import parserpart2


class ASTNode(object):
    def __init__(self,val = '',realval = '',lineno = -1,pos = -1)
        self.val = val                  #tok.type_ same as TK_IF, TK_INT etc
        self.realval = realval          #Actual text of the lexeme
        self.lineno = lineno
        self.pos = pos
        self.children = []


class ASTClass(object):
    def __init__(self,PTHead):
        self.ASTHead = ASTNode(val=PTHead.val)

    def traverse(PTobj,val)
        if PTobj.val == val:
            return PTobj
        else
            if PTobj.children:
                for child in PTobj.children:
                    traverse(child,val)


    def CreateAST(self,PTobj,ASTobj):
        if(PTobj.val == '<assignm_stmt>'):
            newnode = ASTNode()
            newnode.realval = 'TK_ASSIGN'
            leftchild = ASTNode()
            temp = traverse(PTobj.children[0],'TK_ID')
            leftchild.val = temp.val
            leftchild.realval = temp.realval
            leftchild.lineno = temp.lineno
            leftchild.pos = temp.pos
            newnode.children.append(leftchild)
            rightchild = ASTNode()
            
            
        
        if(PTobj.val == '<arithmetic_expression>'):
            
