from __future__  import annotations


from typing import TYPE_CHECKING


from synthesis.baseDSL.mainBase.node import Node
from synthesis.baseDSL.mainBase.noTerminal import NoTerminal
from synthesis.baseDSL.util.control import Control

if TYPE_CHECKING:
    from synthesis.ai.Interpreter import Interpreter
    from synthesis.baseDSL.util.factory import Factory



from abc import ABC, abstractmethod





from game.unit import Unit
from game.gameState import GameState


class ChildC(Node,ABC):
    pass
    

class C(Node,NoTerminal):

    
        
    def __init__(self, childC : ChildC = None):
        self._childC = childC
        
    def translate2(self) -> str:
        return self._childC.translate2()
   
  
    def translate(self) -> str:
        return "C" if self._childC == None else self._childC.translate()
    
   
    def  translateIndentation(self,n_tab:int) ->str:
        tabs = ""
        for _ in range(n_tab):
            tabs+="\t"
        return tabs+"C" if self._childC == None else self._childC.translateIndentation(int)
            
    
    
    def interpret(self,gs : GameState, player:int, u : Unit, automata :Interpreter) -> None:
        self._childC.interpret(gs,player,u,automata)
   
   
   
    def getRule(self)->Node:
        return self._childC
    
    
    def setRule(self, node : Node)->None:
        if  issubclass(node,ChildC):
            self._childC = node
    
    
    def rules(self,f: Factory) :#->list[Node]
        return [f.build_Attack(),f.build_Build(),f.build_Train(),
                f.build_AttackIfrange(),f.build_MoveAway(),f.build_MoveToUnit(),
                f.build_Harvest()]
        
        
    def load(self,List : list[str], f : Factory) -> None:
        s1 = List.pop(0)
        n1 = Control.aux_load(s1, f)
        n1.load(List, f)
        self._childC = n1
	



    def save(self,l : list[str]) -> None:
        l.append("C")
        self._childC.save(l)
        
    
    def clone(self, f : Factory) -> Node:
        if self._childC == None: return f.build_C()
        return f.build_C(self._childC.clone(f))
    
    def resert(self, f : Factory) -> None:
        if self._childC == None: self._childC.resert(f)
        
    def clear(self,father:Node, f : Factory) -> Node:
        
        childwasuse = self._childC.clear(self,f)
        if not childwasuse:
            father._childS= f.build_Empty()
            return False

		
        return True; 