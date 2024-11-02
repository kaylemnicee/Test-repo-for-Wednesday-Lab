from game.gameState import GameState
from game.unit import Unit
from synthesis.ai.Interpreter import Interpreter
from synthesis.baseDSL.almostTerminal.targetPlayer import TargetPlayer
from synthesis.baseDSL.mainBase.c import C, ChildC
from synthesis.baseDSL.mainBase.node import Node
from synthesis.baseDSL.almostTerminal.opponentPolicy import OpponentPolicy


from synthesis.baseDSL.util.factory import Factory



class MoveAway(ChildC,Node):
    
    def __init__(self) -> None:
        self._used = False
        pass
        
  
    
    def translate(self) -> str:
        return "u.moveAway()"
    
    def translate2(self) -> str:
        return "u.moveAway()"
    
    def  translateIndentation(self,n_tab:int) ->str:
        tabs = ""
        for _ in range(n_tab):
            tabs+="\t"
        return tabs + "u.moveAway()"
        
    
    
    def interpret(self,gs : GameState, player:int, u : Unit, automata :Interpreter) -> None:
        
        pgs = gs.getPhysicalGameState()
        if u.getType().getCanMove() and u.getPlayer()==player and automata._memory._freeUnit[u.getID()]  :
            u2 = automata.farthestAllyBase(pgs,player,u)
            if(u2!=None) :
                pf =  automata._core._pf
                move = pf.findPathToPositionInRange(u, u2.getX() + u2.getY() * pgs.getWidth(),1, gs )
                if  move!=None :
                    x=u.getX()
                    y=u.getY()
                    if move.getDirection() == move.getDIRECTION_DOWN():y+=1
                    if move.getDirection() == move.getDIRECTION_UP():y-=1
                    if move.getDirection() == move.getDIRECTION_LEFT():x-=1
                    if move.getDirection() == move.getDIRECTION_RIGHT():x+=1
                    self._used = True
                    automata._core.move(u, x, y)
                    automata._memory._freeUnit[u.getID()] = False
					
					
    def load(self, l : list[str], f :Factory):
        pass
	

    def save(self, l : list[str]):
        l.append("MoveAway")
        
    def clone(self, f : Factory) -> Node:
        return f.build_MoveAway()
    
    def resert(self, f : Factory) -> None:
        self._used = False
        
    def clear(self,father:Node, f : Factory) -> Node:
        return self._used
         
	
   
        
