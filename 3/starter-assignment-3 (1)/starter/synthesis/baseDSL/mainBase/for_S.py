from __future__  import annotations
from typing import TYPE_CHECKING






if TYPE_CHECKING:
    from synthesis.baseDSL.util.factory import Factory



from synthesis.baseDSL.mainBase.S import ChildS,S

from game.unit import Unit
from game.gameState import GameState

from game.physicalGameState import PhysicalGameState
from synthesis.ai.Interpreter import Interpreter

from synthesis.baseDSL.mainBase.node import Node
from synthesis.baseDSL.util.control import Control


class For_S(ChildS,Node):
    
   
        
    def __init__(self, s : S=S()):
        self._s = s
        
    def translate(self) -> str:
        return "for(Unit u){" +self._s.translate()+"}"
    
    def translate2(self) -> str:
        return "for(Unit u){|" +self._s.translate2()+"|}endFor"
   
    def  translateIndentation(self,n_tab:int) ->str:
        tabs = ""
        for _ in range(n_tab):
            tabs+="\t"
        return tabs+ "for(Unit u){\n" + \
            self._s.translateIndentation(n_tab+1)+"\n"+\
				tabs+"}"
            
    
    
    def interpret(self,gs : GameState, player:int, u : Unit, automata :Interpreter) -> None:
        pgs:PhysicalGameState = gs.getPhysicalGameState()
        for u2 in pgs.getUnits().values():
            
            if u2.getPlayer()==player and automata._core.getAbstractAction(u2)==None :
                self._s.interpret(gs, player,u2, automata)
   
   
    def load(self,l:list[str], f: Factory) -> None:
       
        s = l.pop(0)
        n = Control.aux_load(s, f)
        n.load(l, f)
        self._s =  n
		

    def save(self,l : list[str]) -> None:
        l.append("For_S")
        self._s.save(l)
        
    def clone(self, f : Factory) -> Node:
        return f.build_For_S(self._s.clone(f))
    
    def resert(self, f : Factory) -> None:
        if self._s == None: self._s.resert(f)
        
    def clear(self,father:Node, f : Factory) -> Node:
        
        if isinstance(self._s._childS, For_S):
            self._s = f.build_S(self._s._childS)
		
        childwasuse = self._s.clear(self,f)
        if not childwasuse:				
			
            father.childS= f.build_Empty()
            return False

        return True
    

	
   