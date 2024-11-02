
from game.gameState import GameState
from game.unit import  Unit
from synthesis.ai.Interpreter import Interpreter
from synthesis.baseDSL.almostTerminal.opponentPolicy import OpponentPolicy
from synthesis.baseDSL.mainBase.c import C, ChildC
from synthesis.baseDSL.mainBase.node import Node


from synthesis.baseDSL.mainBase.c import ChildC,C
from synthesis.baseDSL.util.factory import Factory


class Attack(ChildC,Node):
    
   
        
    def __init__(self,op :OpponentPolicy=None) -> None:
        self._used = False
        self._op =op 
        
    
    def translate(self) -> str:
        return "u.attack("+self._op.getValue()+")"
    
    def translate2(self) -> str:
        return "u.attack(|"+self._op.getValue()+"|)"
    
    
    def  translateIndentation(self,n_tab:int) ->str:
        tabs = ""
        for _ in range(n_tab):
            tabs+="\t"
        return tabs +"u.attack("+self._op.getValue()+")"
        
    
    
    def interpret(self,gs : GameState, player:int, u : Unit, automata :Interpreter) -> None:
        p = gs.getPlayer(player)
        if (not u.getType().getCanAttack()) or u.getPlayer() != player :
            return 
	    
        if  automata._memory._freeUnit[u.getID()] :
           
            target = self._op.getUnit(gs, p, u, automata)
            self._used = True
            automata._core.attack(u, target)
            automata._memory._freeUnit[u.getID()] = False
         
	
    def load(self, l : list[str], f : Factory):
        s = l.pop(0)
        self._op =  f.build_OpponentPolicy(s)
	



    def save(self,l : list[str])->None:
        l.append("Attack")
        l.append(self._op.getValue())



    def clone(self, f : Factory) -> Node:
        return f.build_Attack(self._op.clone(f))
    
    def resert(self, f : Factory) -> None:
        self._used = False
        
    def clear(self,father:Node, f : Factory) -> Node:
        return self._used