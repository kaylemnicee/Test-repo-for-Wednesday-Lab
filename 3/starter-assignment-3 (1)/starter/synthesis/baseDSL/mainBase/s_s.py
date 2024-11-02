from __future__  import annotations


from typing import TYPE_CHECKING

from synthesis.ai.Interpreter import Interpreter
from synthesis.baseDSL.mainBase.node import Node
from synthesis.baseDSL.mainBase.S import S, ChildS
from synthesis.baseDSL.util.control import Control



if TYPE_CHECKING:
    from synthesis.baseDSL.util.factory import Factory





from game.physicalGameState import PhysicalGameState

from game.unit import Unit
from game.gameState import GameState



class S_S(ChildS,Node):
    
    
        
    def __init__(self, sL : S = S(), sR : S=S()):
        self._sLeft = sL
        self._sRight = sR
        
    def translate(self) -> str:
        return self._sLeft.translate()+" "+self._sRight.translate()
    
    def translate2(self) -> str:
        return self._sLeft.translate2()+"|"+self._sRight.translate2()
   
    def  translateIndentation(self,n_tab:int) ->str:
        tabs = ""
        for _ in range(n_tab):
            tabs+="\t"
        return tabs+ self._sLeft.translateIndentation(n_tab)+"\n"+self._sRight.translateIndentation(n_tab)
            
    
    
    def interpret(self,gs : GameState, player:int, u : Unit, automata :Interpreter) -> None:
        self._sLeft.interpret(gs, player, u, automata)
        self._sRight.interpret(gs, player, u, automata)
   
   
   
    def load(self,l : list[str], f : Factory)->None:
	
        s = l.pop(0)
        n = Control.aux_load(s, f)
        n.load(l, f)
        self._sLeft =  n
        s1 = l.pop(0)
        n1 = Control.aux_load(s1, f)
        n1.load(l, f)
        self._sRight =  n1





    def save(self,l : list[str]) ->None:
        l.append("S_S")
        self._sLeft.save(l)
        self._sRight.save(l)
        
        
    def clone(self, f : Factory) -> Node:
        
        return f.build_S_S(self._sLeft.clone(f),self._sRight.clone(f))
    
    def resert(self, f : Factory) -> None:
        if self._sLeft !=None  :self._sLeft.resert()
        if self._sRight!=None  :self._sRight.resert()
        
    def clear(self,father:Node, f : Factory) -> bool:
        childwasuse1 = self._sLeft.clear(self,f)
        childwasuse2 = self._sRight.clear(self,f)
        if not childwasuse1 and  not childwasuse2:		
            father._childS = f.build_Empty()
            return False
		
		
        if not childwasuse1:			
            father._childS = self._sRight._childS
            return True


        if not childwasuse2 :			
            father._childS = self._sLeft._childS
            return True

		
        return True; 