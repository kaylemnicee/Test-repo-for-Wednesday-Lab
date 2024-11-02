
from evaluators.evaluator import Evaluator
from game.gameState import GameState
import time
from game.playerAction import PlayerAction
from game.screen import ScreenMicroRTS
from ai.ai import AI
from ai.rush.CombatRush import CombatRush
from game.physicalGameState import PhysicalGameState
from game.unitTypeTable import UnitTypeTable


class SimpleMatch:
    
    def playout(self,gs_a :GameState,ai0 : AI,ai1:AI,player :int,max_tick : int,show_scream:bool,assistant_evaluator:Evaluator=None)->int:
        gs = gs_a.clone()
        ai0.reset()
        ai1.reset()
        if assistant_evaluator!=None:#the evaluator only evaluates the player ai0
            assistant_evaluator.reset()
    
        if show_scream :
            screen = ScreenMicroRTS(gs)
        show = True
        
        while not gs.gameover() and gs.getTime()<max_tick:
            if assistant_evaluator!=None:
                assistant_evaluator.analysis(gs,player,False)
            if show and show_scream   :
                    screen.draw()
                    time.sleep(0.1) 

            ini_time = time.time()
            try:
                pa0 :  PlayerAction =ai0.getActions(gs,player)
            except Exception as e:
                return 1-player  , -1
            timeP0 = time.time()- ini_time
            
            ini_time = time.time()  
            pa1 = ai1.getActions(gs,1 -player)
            timeP1 = time.time()- ini_time
            
            if timeP0>0.110 and timeP1>0.110:
                return -1,-1
            elif timeP0>0.110 :
                return 1- player,-1
            elif timeP1>0.110:
                return player,-1
            
            if show_scream:show = gs.updateScreen()
              
            gs.issueSafe(pa0)
            gs.issueSafe(pa1)      
            gs.cycle()
        if assistant_evaluator!=None:
            assistant_evaluator.analysis(gs,player,True)
          
        if assistant_evaluator!=None:   
    
            return gs.winner() ,assistant_evaluator.getValue()#the evaluator only evaluates the player ai0
        
        return gs.winner(), 0
    
    @staticmethod
    def test():
        map = "./maps/basesWorkers32x32A.xml"
        utt = UnitTypeTable(2)
        pgs = PhysicalGameState.load(map,utt)
        gs = GameState(pgs,utt)
        ai0 = CombatRush(pgs,utt,"Light")
        ai1 = CombatRush(pgs,utt,"Heavy")
        sm = SimpleMatch()
        r = sm.playout(gs,ai0,ai1,0,3000,True)
     
        print("win = ",r[0])

            
