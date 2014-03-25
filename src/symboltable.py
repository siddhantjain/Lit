class symbolTable:
    def __init__(self,name,token,lineoccur):        #TODO:Extend definition of Symbol Table
        self.name = name
        self.token = token
        self.lineoccur = lineoccur
    def __str__(self):
        return "Name = %s | Token = %s | Line of occurence = %d "%(self.name,self.token,self.lineoccur)

