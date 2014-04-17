import parserpart2


class ASTNode(object):
    def __init__(self,val = '',realval = '',lineno = -1,pos = -1, idarray = 0):
        self.val = val                  #tok.type_ same as TK_IF, TK_INT etc
        self.realval = realval          #Actual text of the lexeme
        self.lineno = lineno
        self.pos = pos
        self.idarray = idarray
        self.children = []
    
    def CopyValues(ASTobj,PTobj):
        ASTobj.val = PTobj.val
        ASTobj.realval = PTobj.realval
        ASTobj.lineno = PTobj.lineno
        ASTobj.pos = PTobj.pos
        if PTobj.children:
            ASTobj.children = PTobj.children[:]
        else:
            ASTobj.children = []
        return ASTobj


class PassByRefNumber(object):
    def __init__(self,val):
        self.val = val
        


class ASTClass(object):
    def __init__(self,PTHead):
        self.ASTHead = ASTNode(val=PTHead.val)

    def PTtraverse(self,PTobj,val):
        if PTobj.val == val:
            #print('In traverse:%s'%PTobj.val)
            return PTobj
        elif PTobj.children:
            for child in PTobj.children:
                #print('In traverse mismatch:%s'%child.val)
                return self.PTtraverse(child,val)
                

    def CreateAST1(self,PTobj,tag):
        if(tag == '<id>'):
            newnode = ASTNode()
            PTobj = self.PTtraverse(PTobj,'<id>')
            temp = self.PTtraverse(PTobj,'TK_ID')
            #print('temp=%s'%temp.val)
            newnode = ASTNode.CopyValues(newnode,temp)
            #print('PTobjchild=%s'%PTobj.children[1].val)
            temp = self.PTtraverse(PTobj.children[1],'<id_1>')
            #print('temp2=%s'%temp.val)
            
            if temp.children:
                #newnode.val = newnode.val + '['
                newnode2 = ASTNode()
                #print('Reached here: %s'%temp.children[1].children[0].val)
                if(temp.children[1].children[0].val=='TK_NUM' or temp.children[1].children[0].val=='TK_ID'):
                    newnode2 = ASTNode.CopyValues(newnode2,temp.children[1].children[0])
                    #print('array index: %s'%newnode2.val)
                    newnode.idarray = 1
                #newnode.val = newnode.val + ']'
                newnode.children.append(newnode2)
            return newnode
        
        elif(tag=='<parameter_list>'):
            newnode = ASTNode()
            newnode = ASTNode.CopyValues(newnode,PTobj.children[0].children[0])         #Data Type of Parameter INT or FLOAT
            newnode2 = ASTNode()
            newnode2 = ASTNode.CopyValues(newnode2,PTobj.children[1])         #Variable details
            newnode.children.append(newnode2)
            return newnode
        
        elif(tag == '<declrtv_stmt>'):
            newnode = ASTNode()
            newnode = ASTNode.CopyValues(newnode,PTobj.children[0].children[0])         #Data Type of Variable INT or FLOAT
            newnode2 = ASTNode()
            newnode2 = ASTNode.CopyValues(newnode2,PTobj.children[1])
            if (PTobj.children[2].children[0] == '<global_stmt>'):                      #If Single Variable Not Array
                if PTobj.children[2].children[0].children:                              #If Variable is global type
                    newnode3 = ASTNode()
                    newnode3 = ASTNode.CopyValues(newnode3,PTobj.children[2].children[0].children[0])
                    newnode2.children.append(newnode3)
                    
            elif(PTobj.children[2].children[0] == 'TK_CSQ'):                      #If Array
                newnode3 = ASTNode()
                newnode3 = ASTNode.CopyValues(newnode3,PTobj.children[2].children[1])
                newnode.idarray = 1
                newnode2.children.append(newnode3)
                
            newnode.children.append(newnode2)
            return newnode
    
    def GetNoofFunc(self,PTobj,nooffunc):
        if PTobj.children:
            for child in PTobj.children:
                if(child.val == '<function>'):
                    nooffunc.val+=1
                elif(child.val == '<O_functions>'):
                    self.GetNoofFunc(child,nooffunc)
                    
                    
    
    def BuildAST(self,ASTobj,PTobj):
        if(PTobj.val == '<Program>'):
            for child in PTobj.children:
                #print(child.val)
                ASTobj = self.BuildAST(ASTobj,child)
            return ASTobj
        
        elif(PTobj.val == '<O_functions>'):
            if PTobj.children:
                #print('flag 1 %s'%PTobj.children[0].val)
                ASTNodefunc = self.BuildAST(ASTobj,PTobj.children[0])
                ASTobj.children.append(ASTNodefunc)                     #Append function AST Node to <Program> node
                ASTobj = self.BuildAST(ASTobj,PTobj.children[1])
            
            return ASTobj
        
        elif(PTobj.val == '<function>'):
            ASTNodefuncname = ASTNode()
            #print(PTobj.val)
            ASTNodefuncname = ASTNode.CopyValues(ASTNodefuncname,PTobj.children[0])
            ASTNodeIPP = self.BuildAST(ASTobj,PTobj.children[1])                #Input Parameters
            ASTNodefuncname.children.append(ASTNodeIPP)
            ASTNodeOPP = self.BuildAST(ASTobj,PTobj.children[2])                #Output Parameters
            ASTNodefuncname.children.append(ASTNodeOPP)
            if PTobj.children[4].children:                    #If function contains any statements - decl, other, return
                ASTNodeDeclStmts = ASTNode(val = PTobj.children[4].children[0].val)
                ASTNodeDeclStmts = self.BuildAST(ASTNodeDeclStmts,PTobj.children[4].children[0])
                ASTNodefuncname.children.append(ASTNodeDeclStmts)
            return ASTNodefuncname
            
        elif(PTobj.val == '<input_parameters>'):
            ASTNodeIPP = ASTNode()
            ASTNodeIPP = ASTNode.CopyValues(ASTNodeIPP,PTobj.children[0])
            if(PTobj.children[2].children[0].val == '<parameter_list>'):
                #temp = self.PTtraverse(PTobj,'<parameter_list>')
                #ASTNodeArg = self.BuildAST(ASTNodeIPP,temp)
                ASTNodeArg = self.BuildAST(ASTNodeIPP,PTobj.children[2].children[0])
            #elif(PTobj.children[2].children[0].val == 'TK_VOID')
            return ASTNodeIPP
        
        elif(PTobj.val == '<output_parameters>'):
            ASTNodeOPP = ASTNode()
            ASTNodeOPP = ASTNode.CopyValues(ASTNodeOPP,PTobj.children[0])
            if(PTobj.children[2].children[0].val == '<parameter_list>'):
                #temp = self.PTtraverse(PTobj,'<parameter_list>')
                #ASTNodeArg = self.BuildAST(ASTNodeIPP,temp)
                ASTNodeArg = self.BuildAST(ASTNodeOPP,PTobj.children[2].children[0])
            #elif(PTobj.children[2].children[0].val == 'TK_VOID')
            return ASTNodeOPP
            
        elif(PTobj.val=='<parameter_list>'):
            ASTNodeArg = self.CreateAST1(PTobj,'<parameter_list>')
            ASTobj.children.append(ASTNodeArg)
            if PTobj.children[2].children:                  #Checking for more agruments with <next_pl>
                ASTobj = self.BuildAST(ASTobj,PTobj.children[2].children[1])
            return ASTobj
        
        elif(PTobj.val == '<declrtv_stmts>'):
            if PTobj.children:
                #ASTNodeDeclStmts = ASTNode(val = PTobj.val)
                ASTobj = self.BuildAST(ASTobj,PTobj.children[0])            #Call function back <declrtv_stmt>
                ASTobj = self.BuildAST(ASTobj,PTobj.children[1])            #Check for more declarations
            return ASTobj
        
        elif(PTobj.val == '<declrtv_stmt>'):
            ASTNodeDeclVar = self.CreateAST1(PTobj,'<declrtv_stmt>')
            ASTobj.children.append(ASTNodeDeclVar)
            return ASTobj
        
        elif(PTobj.val=='<id>'):
            #print(PTobj.val)
            ASTNodeid = self.CreateAST1(PTobj,'<id>')
            ASTobj.children.append(ASTNodeid)
            return ASTobj
        
            
            
        
    
                
        else:
            if PTobj.children:
                for child in PTobj.children:
                    #print(child.val)
                    ASTobj = self.BuildAST(ASTobj,child)
            return ASTobj

    def PrintAST(self,obj,level):
        temp = '\t'*level + obj.val
        print('%s'%temp)
        level+=1;
        for child in obj.children:
            self.PrintAST(child,level)    
    
    
    def CreateAST(self,PTobj,ASTobj):
        if(PTobj.val == '<assignm_stmt>'):
            newnode = ASTNode()
            newnode.realval = 'TK_ASSIGN'
            leftchild = ASTNode()
            temp = PTtraverse(PTobj.children[0],'TK_ID')
            leftchild.val = temp.val
            leftchild.realval = temp.realval
            leftchild.lineno = temp.lineno
            leftchild.pos = temp.pos
            newnode.children.append(leftchild)
            rightchild = ASTNode()
            
            
        
        if(PTobj.val == '<arithmetic_expression>'):
            newnode = ASTNode();
            
