from game.gameState import GameState
from game.player import Player
from game.unit import Unit
from synthesis.baseDSL.almostTerminal.almostTerminal import AlmostTerminal
from synthesis.ai.Interpreter import Interpreter

from synthesis.baseDSL.util.factory import Factory



class OpponentPolicy(AlmostTerminal):
    

    def __init__(self,op= None) -> None:
        self._op = op
    
    
    def rules(self):#->list[str]:
        return ["Strongest",
		        "Weakest",
		        "Closest",
                "LessHealthy",
		        "MostHealthy"]
    
    @classmethod
    def getName(cls)->str:
        return cls.__name__
    
    def setValue(self, s :str)->None:
        self._op=s
    
    def getValue(self)->str:
        return self._op
	
    def translate(self)->str:
        return self._op
    
    
    def clone(self, f: Factory):
        return f.build_OpponentPolicy(self.getValue())
    
    def  getUnit(self, gs :GameState, p: Player, u:Unit, automata :Interpreter )-> Unit:
		
        if self._op == "Strongest":
            return automata.getUnitStrongest(gs, p, u)

        if self._op == "Weakest":
            return automata.getUnitWeakest(gs, p, u)
  
        if self._op == "Closest":
            u2 = automata.getUnitClosest(gs, p, u)
     
            return u2
  
        if self._op == "Farthest":
            return automata.getUnitFarthest(gs, p, u)
    
        if self._op == "LessHealthy":
            u2 = automata.getUnitClosest(gs, p, u)
          
            return u2
    
        if self._op == "MostHealthy":
            return automata.getUnitMostHealthy(gs, p, u)
    
        return None
      
	