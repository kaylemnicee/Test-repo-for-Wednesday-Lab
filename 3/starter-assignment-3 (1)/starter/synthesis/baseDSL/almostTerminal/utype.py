from synthesis.baseDSL.almostTerminal.almostTerminal import AlmostTerminal


from synthesis.baseDSL.util.factory import Factory



class Utype(AlmostTerminal):
    
   
    def __init__(self,utype=None) -> None:
        self._type = utype
    
    
    def rules(self):#->list[str]:
        return ["Base",
		        "Barracks",
                "Worker",
                "Ranged",
                "Light",
		        "Heavy"]
    
   
    
    def setValue(self, s :str)->None:
        self._type=s
    
    def getValue(self)->str:
        return self._type
	
    def translate(self)->str:
        return self._type
    
    def clone(self, f: Factory):
        return f.build_Utype(self.getValue())