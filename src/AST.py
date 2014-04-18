import parserpart2
from data import terminals, nonTerminals


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
        if PTobj.val in terminals:
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
        #print('Reached Here 1 %s'%PTHead.val)
        self.ASTHead = ASTNode(val=PTHead.val)
        #print('Reached Here 1 %s'%self.ASTHead.val)

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
                #print('Reached Here 2 %s'%ASTobj.val)
                ASTobj = self.BuildAST(ASTobj,child)
            return ASTobj
        
        elif(PTobj.val == '<O_functions>'):
            if PTobj.children:
                #print('flag 1 %s'%PTobj.children[0].val)
                ASTNodefunc = self.BuildAST(ASTobj,PTobj.children[0])
                ASTobj.children.append(ASTNodefunc)                     #Append function AST Node to <Program> node
                ASTobj = self.BuildAST(ASTobj,PTobj.children[1])
            
            return ASTobj
        
        elif(PTobj.val == '<main_function>'):
            ASTNodeMain = ASTNode()
            ASTNodeMain = ASTNode.CopyValues(ASTNodeMain,PTobj.children[0])
            if PTobj.children[1].children:                    #If function contains any statements - decl, other, return
                #Gets all declarations under one node
                ASTNodeDeclStmts = ASTNode(val = PTobj.children[1].children[0].val)
                ASTNodeDeclStmts = self.BuildAST(ASTNodeDeclStmts,PTobj.children[1].children[0])
                ASTNodeMain.children.append(ASTNodeDeclStmts)
                #Gets all statements in the function under one node
                ASTNodeOStmts = ASTNode(val = PTobj.children[1].children[1].val)
                #print('Reached here %s'% PTobj.children[4].children[1].val)
                ASTNodeOStmts = self.BuildAST(ASTNodeOStmts,PTobj.children[1].children[1])          #Call with <O_stmts>
                ASTNodeMain.children.append(ASTNodeOStmts)
                #Gets return statement
                ASTNodeRet = ASTNode()
                ASTNodeRet = self.BuildAST(ASTNodeRet,PTobj.children[1].children[2])
                ASTNodeMain.children.append(ASTNodeRet)
            ASTobj.children.append(ASTNodeMain)
            return ASTobj
        
        
        
        elif(PTobj.val == '<function>'):
            #Each function is representaed by its TK_FUNC token
            #A function has the following children - TK_IPP,TK_OPP,<declrtv_stmts>,<O_stmts>,<return_stmt>.
            ASTNodefuncname = ASTNode()
            #print(PTobj.val)
            ASTNodefuncname = ASTNode.CopyValues(ASTNodefuncname,PTobj.children[0])
            ASTNodeIPP = self.BuildAST(ASTobj,PTobj.children[1])                #Input Parameters
            ASTNodefuncname.children.append(ASTNodeIPP)
            ASTNodeOPP = self.BuildAST(ASTobj,PTobj.children[2])                #Output Parameters
            ASTNodefuncname.children.append(ASTNodeOPP)
            if PTobj.children[4].children:                    #If function contains any statements - decl, other, return
                #Gets all declarations under one node
                ASTNodeDeclStmts = ASTNode(val = PTobj.children[4].children[0].val)
                ASTNodeDeclStmts = self.BuildAST(ASTNodeDeclStmts,PTobj.children[4].children[0])
                ASTNodefuncname.children.append(ASTNodeDeclStmts)
                #Gets all statements in the function under one node
                ASTNodeOStmts = ASTNode(val = PTobj.children[4].children[1].val)
                #print('Reached here %s'% PTobj.children[4].children[1].val)
                ASTNodeOStmts = self.BuildAST(ASTNodeOStmts,PTobj.children[4].children[1])          #Call with <O_stmts>
                ASTNodefuncname.children.append(ASTNodeOStmts)
                #Gets return statement
                ASTNodeRet = ASTNode()
                ASTNodeRet = self.BuildAST(ASTNodeRet,PTobj.children[4].children[2])
                ASTNodefuncname.children.append(ASTNodeRet)
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
        
        elif(PTobj.val == '<O_stmts>'):
            #print('Reached Here 2 %s' %PTobj.val)
            if PTobj.children:
                #print('Reached Here 3 %s' %PTobj.children[0].val)
                ASTobj = self.BuildAST(ASTobj,PTobj.children[0])            #Call function back <stmt>
                ASTobj = self.BuildAST(ASTobj,PTobj.children[1])            #Check for more statements
            return ASTobj
        
        elif(PTobj.val=='<stmt>'):
            #print('Reached Here 3 %s' %PTobj.children[0].val)
            ASTNodeStmt = ASTNode()                                         #Create one node for the entire statement
            ASTNodeStmt = self.BuildAST(ASTNodeStmt,PTobj.children[0])       #Call function back with statement type
            ASTobj.children.append(ASTNodeStmt)
            return ASTobj
        
        elif(PTobj.val=='<gen_stmt>'):
            if(PTobj.children[0].val == '<print_stmts>'):
                ASTobj = ASTNode.CopyValues(ASTobj,PTobj.children[0].children[0].children[0])       #Pivot is either TK_PRINT/TK_PRINTLN
                all_var_node = PTobj.children[0].children[0].children[2]
                if all_var_node.children[0].val in terminals:               #either TK_NUM/TK_RNUM/TK_STRLIT
                    ASTNodePTerm = ASTNode()
                    ASTNodePTerm = ASTNode.CopyValues(ASTNodePTerm,all_var_node.children[0])
                    ASTobj.children.append(ASTNodePTerm)
                elif(all_var_node.children[0].val == '<id>'):
                    ASTobj = self.BuildAST(ASTobj,all_var_node.children[0])
            elif(PTobj.children[0].val == '<read_stmt>'):
                ASTobj = ASTNode.CopyValues(ASTobj,PTobj.children[0].children[0])       #Pivot is TK_READ
                ASTobj = self.BuildAST(ASTobj,PTobj.children[0].children[2])
            return ASTobj
            
            
            
            
        elif(PTobj.val=='<iterative_stmt>'):
            ASTobj = ASTNode.CopyValues(ASTobj,PTobj.children[0])           #TK_WHILE node is pivot for iterative statement
            ASTNodeBE = self.BuildAST(ASTobj,PTobj.children[2])           #Boolean Expression Node
            ASTobj.children.append(ASTNodeBE)
            ASTNodeOStmts = ASTNode(val = PTobj.children[4].val)               #<O_stmts> pivot for all statements in while
            ASTNodeOStmts = self.BuildAST(ASTNodeOStmts,PTobj.children[4])
            ASTobj.children.append(ASTNodeOStmts)
            return ASTobj
            
        elif(PTobj.val=='<Boolean_expression>'):
            ASTNodeBE = ASTNode()
            ASTNodeBE = ASTNode.CopyValues(ASTNodeBE,PTobj)
            #print('Printing BE')
            #self.PrintASTtoTerm(ASTNodeBE,0)
            return ASTNodeBE
        
        elif(PTobj.val=='<cond_stmt>'):
            ASTobj = ASTNode.CopyValues(ASTobj,PTobj.children[0])       #Pivot for cond_stmt is TK_IF
            ASTNodeBE = self.BuildAST(ASTobj,PTobj.children[2])           #Boolean Expression Node
            ASTobj.children.append(ASTNodeBE)
            ASTNodeOStmts = ASTNode(val = PTobj.children[4].val)               #<O_stmts> pivot for all statements in if clause
            ASTNodeOStmts = self.BuildAST(ASTNodeOStmts,PTobj.children[4])
            ASTobj.children.append(ASTNodeOStmts)
            if(PTobj.children[5].children[0].val=='TK_ELSE'):
                ASTNodeElse = ASTNode()
                ASTNodeElse = ASTNode.CopyValues(ASTNodeElse,PTobj.children[5].children[0])      #TK_ELSE pivot for all statements in else clause
                ASTNodeElse = self.BuildAST(ASTNodeElse,PTobj.children[5].children[1])
                ASTobj.children.append(ASTNodeElse)
            
            return ASTobj
                
        elif(PTobj.val == '<return_stmt>'):
            ASTobj = ASTNode.CopyValues(ASTobj,PTobj.children[0])       #TK_RET is pivot for return statements. Children are return ids
            if(PTobj.children[1].children[0].val == 'TK_OSQ'):
                ASTobj = self.BuildAST(ASTobj,PTobj.children[1].children[1])
            return ASTobj
        
        elif(PTobj.val == '<list_var>'):
            ASTobj = self.BuildAST(ASTobj,PTobj.children[0])
            if PTobj.children[1].children:
                ASTobj = self.BuildAST(ASTobj,PTobj.children[1].children[1])
            return ASTobj
        
        elif(PTobj.val=='<funcall_Stmt>'):
            ASTobj = ASTNode.CopyValues(ASTobj,PTobj.children[0])
            ASTNodefuncname = ASTNode()
            ASTNodefuncname = ASTNode.CopyValues(ASTNodefuncname,PTobj.children[1])
            ASTNodefuncname = self.BuildAST(ASTNodefuncname,PTobj.children[3])
            ASTobj.children.append(ASTNodefuncname)
            return ASTobj
        
        
        elif(PTobj.val=='<assignm_stmt>'):
            #print('Reached Here 2 %s'%PTobj.children[0].val)
            if(PTobj.children[0].val=='<id>'):                                  #If it is a regular assignment statement. Not func call
                #print('Reached Here 1')
                ASTobj = ASTNode.CopyValues(ASTobj,PTobj.children[1])       #Creates node for TK_ASSIGN which will pivot <assign_stmt>
                ASTobj = self.BuildAST(ASTobj,PTobj.children[0])            #Adds the leftchild as identifier. Cal function back with <id>
                ASTNodeAE = self.BuildAST(ASTobj,PTobj.children[2])            #Adds rightchild as arithmetic expression
                ASTobj.children.append(ASTNodeAE)
            elif(PTobj.children[0].val=='TK_OSQ'):                                  #If it is a func call with assignment
                ASTobj = ASTNode.CopyValues(ASTobj,PTobj.children[3])       #Creates node for TK_ASSIGN which will pivot <assign_stmt>
                ASTNodeListVar = ASTNode(val = PTobj.children[1].val)
                ASTNodeListVar = self.BuildAST(ASTNodeListVar,PTobj.children[1])
                ASTobj.children.append(ASTNodeListVar)
                ASTNodeFunCall = ASTNode()
                ASTNodeFunCall = self.BuildAST(ASTNodeFunCall,PTobj.children[4])
                ASTobj.children.append(ASTNodeFunCall)
            return ASTobj
        
        elif(PTobj.val=='<arithmetic_expression>'):
            ASTNodeAE = ASTNode()
            ASTNodeAE = ASTNode.CopyValues(ASTNodeAE,PTobj)
            #print('Printing AE')
            #self.PrintAST(ASTNodeAE,0)
            return ASTNodeAE
        
        elif(PTobj.val=='<id>'):
            #print(PTobj.val)
            ASTNodeid = self.CreateAST1(PTobj,'<id>')
            ASTobj.children.append(ASTNodeid)
            return ASTobj

        return ASTobj
        '''
        else:
            if PTobj.children:
                for child in PTobj.children:
                    #print(child.val)
                    ASTobj = self.BuildAST(ASTobj,child)
            return ASTobj
        '''
    
    
    
    def PrintAST(self,obj,ASTfile,level):
        #print('Reached here %s'%obj.val)
        temp = '\t'*level + obj.val + '\n'
        ASTfile.write(temp)
        level+=1;
        if obj.children:
            for child in obj.children:
                self.PrintAST(child,ASTfile,level)    
    
    def PrintASTtoTerm(self,obj,level):
        temp = '\t'*level + obj.val
        print('%s'%temp)
        level+=1;
        if obj.children:
            for child in obj.children:
                self.PrintASTtoTerm(child,level)
    
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
            
