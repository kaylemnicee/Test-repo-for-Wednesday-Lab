from synthesis.baseDSL.almostTerminal.almostTerminal import AlmostTerminal

from synthesis.baseDSL.util.factory import Factory



class TargetPlayer(AlmostTerminal):
    

        
    def __init__(self,tp= None) -> None:
        self._tp = tp
    
    
    def rules(self):#->list[str]:
        return ["Ally",
		        "Enemy"]
    
   
    
    def setValue(self, s :str)->None:
        self._tp=s
    
    def getValue(self)->str:
        return self._tp
	
    def translate(self)->str:
        return self._tp
    
    def clone(self, f: Factory):
        return f.build_TargetPlayer(self.getValue())