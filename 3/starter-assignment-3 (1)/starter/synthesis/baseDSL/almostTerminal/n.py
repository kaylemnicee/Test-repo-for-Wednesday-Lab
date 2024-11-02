from synthesis.baseDSL.almostTerminal.almostTerminal import AlmostTerminal


from synthesis.baseDSL.util.factory import Factory



class N(AlmostTerminal):
    
   
        
    def __init__(self,n= None) -> None:
        self._n = n
    
    
    def rules(self,act=None):#->list[str]:
        if act == "b" or act =="h":
            return ["1","2","3"]
        return ["0",
		        "1",
		        "2",
		        "3",
		        "4",
                "5",
		        "6",
		        "7",
		        "8",
                "9",
                "10",
		        "15",
		        "20",
                "25",
		        "50",
		        "100"]
    
  
    
    def setValue(self, s :str)->None:
        self._n=s
    
    def getValue(self)->str:
        return self._n
	
    def translate(self)->str:
        return self._n
    
    def clone(self, f: Factory):
        return f.build_N(self.getValue())