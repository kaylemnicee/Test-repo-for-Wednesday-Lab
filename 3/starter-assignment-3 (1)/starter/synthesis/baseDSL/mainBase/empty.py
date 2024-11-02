
from __future__  import annotations


from typing import TYPE_CHECKING

from synthesis.baseDSL.mainBase.node import Node

from synthesis.baseDSL.mainBase.S import ChildS

if TYPE_CHECKING:
    from synthesis.ai.Interpreter import Interpreter
    from synthesis.baseDSL.util.factory import Factory

#from synthesis.baseDSL.baseMain.S import ChildS
#from synthesis.baseDSL.baseMain.node import Node



from game.unit import Unit
from game.gameState import GameState
from game.player import Player



class Empty(ChildS,Node):
    
    def __init__(self) -> None:
        
        pass
        
    
        
    
    def translate(self) -> str:
        return "e"
    
    def translate2(self) -> str:
        return "e"
    
    def  translateIndentation(self,n_tab:int) ->str:
        tabs = ""
        for _ in range(n_tab):
            tabs+="\t"
        return tabs +"e"
        
    
    
    def interpret(self,gs : GameState, player:int, u : Unit, automata :Interpreter) -> None:
        pass
                        
                        
    def load(self, l : list[str], f :Factory):
        pass
	

    def save(self, l : list[str]):
        l.append("Empty")
	
    def clone(self, f : Factory) -> Node:
        return f.build_Empty()
    
    def resert(self, f : Factory) -> None:
        pass
        
    def clear(self,father:Node, f : Factory) -> Node:
        return False