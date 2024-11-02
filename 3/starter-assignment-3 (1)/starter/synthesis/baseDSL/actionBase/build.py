from game.gameState import GameState
from game.unit import  Unit
from game.unitAction import  UnitAction
from synthesis.ai.Interpreter import Interpreter
from synthesis.baseDSL.mainBase.c import C, ChildC
from synthesis.baseDSL.mainBase.node import Node
from synthesis.baseDSL.almostTerminal.utype import Utype
from synthesis.baseDSL.almostTerminal.direction import Direction
from synthesis.baseDSL.almostTerminal.n import N


from synthesis.baseDSL.util.factory import Factory


class Build(ChildC,Node):
    
        
    def __init__(self,utype : Utype= None, n : N= None, direc : Direction= None) -> None:
        self._type =utype
        self._n = n
        self._direc = direc
        self._used = False
        
    
    def translate(self) -> str:
        return "u.build("+self._type.getValue()+","+self._direc.getValue()+","+self._n.getValue()+")"
    
    def translate2(self) -> str:
        return "u.build(|"+self._type.getValue()+"|"+self._direc.getValue()+"|"+self._n.getValue()+"|)"
    
    def  translateIndentation(self,n_tab:int) ->str:
        tabs = ""
        for _ in range(n_tab):
            tabs+="\t"
        return tabs + "u.build("+self._type.getValue()+","+self._direc.getValue()+","+self._n.getValue()+")"
        
    
    
    def interpret(self,gs : GameState, player:int, u : Unit, automata :Interpreter) -> None:
        pgs = gs.getPhysicalGameState()
        p = gs.getPlayer(player)
        uType = automata._utt.getUnitTypeString(self._type.getValue())
        
        if not automata._memory._freeUnit[u.getID()] :
            return
         
        if not (uType.getName() == "Barracks" or uType.getName() == "Base" ):
            return
        
        if u.getPlayer() != player or \
                    u.getType().getName() != "Worker" or \
                    automata.resource < uType.getCost()    :
            return
        
        if automata.countConstrution(uType.getName(),player,gs) >= int(self._n.getValue()):
            return 
        
        reservedPositions =  []
	
      
        direction = self._direc.converte(gs, player,u)
        if direction==UnitAction.getDIRECTION_UP() :automata._core.build(u,uType,u.getX(),u.getY()-1)
        elif direction==UnitAction.getDIRECTION_DOWN(): automata._core.build(u,uType,u.getX(),u.getY()+1)
        elif direction==UnitAction.getDIRECTION_LEFT(): automata._core.build(u,uType,u.getX()-1,u.getY())
        elif direction==UnitAction.getDIRECTION_RIGHT(): automata._core.build(u,uType,u.getX()+1,u.getY())
        
        else: automata._core.buildIfNotAlreadyBuilding(u,uType,u.getX(),u.getY(),reservedPositions,p,gs)
        
        self._used= True
        automata.resource -= uType.getCost()
        automata._memory._freeUnit[u.getID()] = False
        
        
        
    def load(self, l : list[str], f : Factory):
        s = l.pop(0)
        self._type = f.build_Utype(s)
        s1 = l.pop(0)
        self._direc =  f.build_Direction(s1)
        s2 = l.pop(0)
        self._n = f.build_N(s2)





    def save(self,l : list[str]) -> None:
        l.append("Build")
        l.append(self. _type.getValue())
        l.append(self._direc.getValue())
        l.append(self._n.getValue())
	
            
        
    def clone(self, f : Factory) -> Node:
        return f.build_Build(self._type.clone(f), self._direc.clone(f), self._n.clone(f))
    
    def resert(self, f : Factory) -> None:
        self._used = False
        
    def clear(self,father:Node, f : Factory) -> Node:
        return self._used
   
        
