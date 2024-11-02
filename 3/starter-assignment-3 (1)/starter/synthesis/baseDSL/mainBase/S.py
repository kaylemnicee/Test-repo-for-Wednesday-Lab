from __future__  import annotations


from typing import TYPE_CHECKING

from synthesis.baseDSL.util.control import Control

from synthesis.baseDSL.mainBase.node import Node
from synthesis.baseDSL.mainBase.noTerminal import NoTerminal
if TYPE_CHECKING:
    from synthesis.baseDSL.mainBase.node import Node
    from synthesis.baseDSL.mainBase.noTerminal import NoTerminal
    from synthesis.baseDSL.util.factory import Factory
    from synthesis.ai.Interpreter import Interpreter
    
    
from abc import ABC, abstractmethod

#from synthesis.baseDSL.baseMain.node import Node
#from synthesis.baseDSL.baseMain.noTerminal import NoTerminal
#from synthesis.baseDSL.util.control import Control


from game.unit import Unit
from game.gameState import GameState


class ChildS(Node,ABC):
    pass
    

class S(Node,NoTerminal):

    
        
    def __init__(self, childS : ChildS = None):
        self._childS : ChildS = childS
        
   
   
  
    def translate(self) -> str:
        return "S" if self._childS == None else self._childS.translate()
    
    
    def translate2(self) -> str:
        return self._childS.translate2()
   
    def  translateIndentation(self,n_tab:int) ->str:
        tabs : str = ""
        for _ in range(n_tab):
            tabs+="\t"
        return tabs+"S" if self._childS == None else self._childS.translateIndentation(n_tab)
            
    
    
    def interpret(self,gs : GameState, player:int, u : Unit, automata :Interpreter) -> None:
        if u!=None:
            if automata._memory._freeUnit[u.getID()] == False:
                return
        self._childS.interpret( gs,player,u,automata)
   
   
   
    def getRule(self)->Node:
        return self._childS
    
    
    def setRule(self, node : Node)->None:
        if  issubclass(node,ChildS):
            self._childS = node
    
    
    def rules(f: Factory) :#->list[Node]
        return [f.build_for_S(),
                f.build_C()]
        
    
    def load(self, l: list[str], f : Factory) -> None:
        s = l.pop(0)
        n = Control.aux_load(s, f)
        n.load(l, f)
        self._childS = n


    def save(self,l : list[str]):
        l.append("S")
        self._childS.save(l)
	
 
    def clone(self, f : Factory) -> Node:
        if self._childS == None: return f.build_S()
        return f.build_S(self._childS.clone(f))
    
    def resert(self, f : Factory) -> None:
        if self._childS == None: self._childS.resert(f)
        
    def clear(self,father:Node, f : Factory) -> Node:
        return self._childS.clear(self, f)