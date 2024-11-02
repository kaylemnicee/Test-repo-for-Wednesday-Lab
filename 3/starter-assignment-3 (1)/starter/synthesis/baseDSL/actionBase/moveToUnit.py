
from game.gameState import GameState
from game.unit import Unit
from synthesis.ai.Interpreter import Interpreter
from synthesis.baseDSL.almostTerminal.targetPlayer import TargetPlayer
from synthesis.baseDSL.mainBase.c import C, ChildC
from synthesis.baseDSL.mainBase.node import Node
from synthesis.baseDSL.almostTerminal.opponentPolicy import OpponentPolicy


from synthesis.baseDSL.util.factory import Factory



class MoveToUnit(ChildC,Node):
    
   
    def __init__(self,op :OpponentPolicy=OpponentPolicy(), tp :TargetPlayer=TargetPlayer()) -> None:
        self._op =op 
        self._tp = tp
        self._used = False
        
    
    def translate(self) -> str:
        return "u.moveToUnit("+self._tp.getValue()+","+self._op.getValue()+")"
    
    def translate2(self) -> str:
        return "u.moveToUnit(|"+self._tp.getValue()+"|"+self._op.getValue()+"|)"
    
    def  translateIndentation(self,n_tab:int) ->str:
        tabs = ""
        for _ in range(n_tab):
            tabs+="\t"
        return tabs +"u.moveToUnit("+self._tp.getValue(),",",self._op.getValue()+")"
        
    
    
    def interpret(self,gs : GameState, player:int, u : Unit, automata :Interpreter) -> None:
        jogador =-1
        if self._tp.getValue() =="Ally":jogador=1-player
        else: jogador = player
        p = gs.getPlayer(jogador)
        pgs = gs.getPhysicalGameState() 
		
        if u.getType().getCanMove() and u.getPlayer()==player and \
                            automata._memory._freeUnit[u.getID()] :
            u2 = self._op.getUnit(gs, p, u, automata)
            
            if u2!=None :
                pf =  automata._core._pf   
                move = pf.findPathToPositionInRange(u, u2.getX() + u2.getY() * pgs.getWidth(),1, gs )
                if move!=None:
                    x=u.getX()
                    y=u.getY()
                    if move.getDirection() == move.getDIRECTION_DOWN():y+=1
                    if move.getDirection() == move.getDIRECTION_UP():y-=1
                    if move.getDirection() == move.getDIRECTION_LEFT():x-=1
                    if move.getDirection() == move.getDIRECTION_RIGHT():x+=1
                    self._used = True
                    automata._core.move(u, x, y)
                    self._used = True
                    automata._memory._freeUnit[u.getID()] = False
			
         
	
    def load(self, l : list[str], f :Factory):
        s = l.pop(0)
        self._tp= f.build_TargetPlayer(s)
        s1 = l.pop(0)
        self._op = f.build_OpponentPolicy(s1)




    def save(self, l : list[str]):
        l.append("MoveToUnit")
        l.append(self._tp.getValue())
        l.append(self._op.getValue())
        
    def clone(self, f : Factory) -> Node:
        return f.build_MoveToUnit(self._tp.clone(f), self._op.clone(f))
    
    def resert(self, f : Factory) -> None:
        self._used = False
        
    def clear(self,father:Node, f : Factory) -> Node:
        return self._used
        
